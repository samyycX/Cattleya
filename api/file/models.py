import urllib
import uuid

import oss2
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import models
from django.forms import model_to_dict
from rest_framework import viewsets, serializers
from rest_framework.authentication import TokenAuthentication
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser, BasePermission
from rest_framework.request import Request
from rest_framework.views import APIView

from api.file.utils import get_file_hash
from api.models import User
from api.renderer import JSONResponseRenderer
from api.utils.result import Result
from cattleya import settings

auth = oss2.Auth(settings.OSS_ACCESS_KEY_ID, settings.OSS_ACCESS_KEY_SECRET)
bucket = oss2.Bucket(auth, settings.OSS_ENDPOINT, settings.OSS_BUCKET_NAME)

class File(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True)
    name = models.CharField(verbose_name="文件名", null=True, blank=True, max_length=256)
    path = models.CharField(verbose_name="文件链接", null=True, blank=True, max_length=8192)
    hash = models.CharField(verbose_name="哈希", max_length=255, unique=True)
    created_by = models.ForeignKey(User, verbose_name="上传者", on_delete=models.DO_NOTHING)
    created_time = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)


class FilePathField(serializers.RelatedField):
    def to_representation(self, value):
        protocol = "https://" if "https://" in settings.OSS_ENDPOINT else "http://"
        raw_endpoint = settings.OSS_ENDPOINT.replace(protocol, "")
        return urllib.parse.urljoin(f"{protocol}{settings.OSS_BUCKET_NAME}.{raw_endpoint}", value)

class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return IsAdminUser().has_permission(request, view) or bool(request.user and request.user.id == obj.created_by)

class FileSerializer(serializers.ModelSerializer):
    path = FilePathField(many=False, read_only=True)
    class Meta:
        model = File
        fields = ("id", "name", "path", "hash", "created_by", "created_time")


class FileViewSet(viewsets.ModelViewSet):
    model = File
    parser_classes = (MultiPartParser,)
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    renderer_classes = (JSONResponseRenderer,)

    permissions_classes_by_action = {
        "list": (IsAuthenticated,),
        "retrieve": (AllowAny,),
        "update": (IsAdminUser,),
        "partial_update": (IsAdminUser,),
        "destroy": (IsOwner,),
        "create": (IsAuthenticated,),
    }

    def create(self, request: Request):
        files = request.FILES.getlist("files")
        if files is None:
            return Result.err(msg="文件为空", code=400)
        for file in files:
            suffix = file.name.split(".")[-1]
            banned_suffixes = []
            if suffix in banned_suffixes:
                return Result.err(msg="不支持此文件格式", code=400)

        fileObjs = []
        for file in files:
            fileObj = File(created_by=request.user)
            split = file.name.split(".")
            suffix = split[-1]
            filename = split[-2]

            full_filename = f"cattleya/file/{filename}.{suffix}"

            hash = get_file_hash(file.file)
            try:
                duplicatedFileObj = File.objects.get(hash=hash)
                fileObjs.append(duplicatedFileObj)
                continue
            except File.DoesNotExist:
                pass
            # auth = oss2.Auth(settings.OSS_ACCESS_KEY_ID, settings.OSS_ACCESS_KEY_SECRET)
            # bucket = oss2.Bucket(auth, settings.OSS_ENDPOINT, settings.OSS_BUCKET_NAME)
            bucket.put_object(full_filename, file)
            fileObj.name = file.name
            fileObj.path = full_filename
            fileObj.hash = hash
            fileObj.save()
            fileObjs.append(fileObj)

        return Result.ok(code=201, msg="上传成功", data=[FileSerializer(fileObj).data for fileObj in fileObjs])

    def destroy(self, request, pk):
        try:
            file = File.objects.get(id=pk)
            bucket.delete_object(file.path)
            file.delete()

            return Result.ok(code=200, msg="删除成功")
        except File.DoesNotExist:
            return Result.err(code=400, msg="文件不存在")