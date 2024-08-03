import urllib
import uuid

import oss2
from django.db import models
from django.forms import model_to_dict
from rest_framework import viewsets, serializers
from rest_framework.authentication import TokenAuthentication
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser, BasePermission
from rest_framework.views import APIView

from api.models import User
from api.utils.result import Result
from cattleya import settings


class File(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True)
    path = models.CharField(verbose_name="文件链接", null=True, blank=True, max_length=8192)
    created_by = models.ForeignKey(User, verbose_name="上传者", on_delete=models.DO_NOTHING)
    created_time = models.DateTimeField(verbose_name="创建时间", auto_now=True)


class FilePathField(serializers.RelatedField):
    def to_representation(self, value):
        protocol = "https://" if "https://" in settings.OSS_ENDPOINT else "http://"
        raw_endpoint = settings.OSS_ENDPOINT.replace(protocol, "")
        return urllib.parse.urljoin(f"{protocol}{settings.OSS_BUCKET_NAME}.{raw_endpoint}", value)

class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return IsAdminUser().has_permission(request, view) or bool(request.user and request.user.id == obj.created_by)

class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ("id", "path", "created_by", "created_time")


class FileViewSet(viewsets.ModelViewSet):
    model = File
    parser_classes = (MultiPartParser,)
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    permissions_classes_by_action = {
        "list": (IsAuthenticated,),
        "retrieve": (AllowAny,),
        "update": (IsAdminUser,),
        "partial_update": (IsAdminUser,),
        "destroy": (IsOwner,),
        "create": (IsAuthenticated,),
    }

    def create(self, request):
        file = request.FILES.get("file")
        if file is None:
            return Result.err(msg="文件为空", code=400)
        suffix = file.name.split(".")[-1]
        banned_suffixes = []
        if suffix in banned_suffixes:
            return Result.err(msg="不支持此文件格式", code=400)

        fileObj = File(created_by=request.user)

        full_filename = f"cattleya/file/{fileObj.id}.{suffix}"
        auth = oss2.Auth(settings.OSS_ACCESS_KEY_ID, settings.OSS_ACCESS_KEY_SECRET)
        bucket = oss2.Bucket(auth, settings.OSS_ENDPOINT, settings.OSS_BUCKET_NAME)
        bucket.put_object(full_filename, file)
        fileObj.path = full_filename
        fileObj.save()

        return Result.ok(code=201, msg="上传成功", data=model_to_dict(fileObj, ("id","path","created_time")))

    def destroy(self, request, pk):
        try:
            file = File.objects.get(id=pk)
            auth = oss2.Auth(settings.OSS_ACCESS_KEY_ID, settings.OSS_ACCESS_KEY_SECRET)
            bucket = oss2.Bucket(auth, settings.OSS_ENDPOINT, settings.OSS_BUCKET_NAME)
            bucket.delete_object(file.path)
            file.delete()

            return Result.ok(code=200, msg="删除成功")
        except File.DoesNotExist:
            return Result.err(code=400, msg="文件不存在")