import base64
import re
import urllib
import uuid

import oss2
from django.contrib.auth import authenticate
from django.contrib.auth.models import AbstractUser
from django.db import models
from rest_framework import serializers, viewsets, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser, BasePermission
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.validators import UniqueValidator
from rest_framework.views import APIView

from api.utils.emoticon import Emoticon
from api.utils.result import Result
from cattleya import settings


class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.id == request.user.id


class User(AbstractUser):
    first_name = None,
    last_name = None,
    nickname = models.CharField(verbose_name="昵称", max_length=15)
    avatar = models.CharField(verbose_name="头像", max_length=150, null=True, blank=True)
    phone = models.CharField(verbose_name="手机号", max_length=30)

    class Meta:
        verbose_name = "用户附加个人资料"


class AvatarField(serializers.RelatedField):
    def to_representation(self, value):
        protocol = "https://" if "https://" in settings.OSS_ENDPOINT else "http://"
        raw_endpoint = settings.OSS_ENDPOINT.replace(protocol, "")
        return urllib.parse.urljoin(f"{protocol}{settings.OSS_BUCKET_NAME}.{raw_endpoint}", value)


class UserSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True, )

    username = serializers.CharField(
        max_length=15,
        allow_blank=False,
        read_only=True,
    )

    nickname = serializers.CharField(
        max_length=15,
        allow_blank=False,
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all(), message="昵称已存在")],
        error_messages={
            "blank": "昵称不能为空",
            "max_length": "昵称不能超过15个字",
        }
    )

    email = serializers.EmailField(
        required=False,
        allow_blank=True,
        error_messages={
            'invalid': "邮箱格式错误"
        }
    )

    phone = serializers.RegexField(
        regex=re.compile(r"^1(3\d|4[5-9]|5[0-35-9]|6[2567]|7[0-8]|8\d|9[0-35-9])\d{8}$"),
        required=False,
        allow_blank=True,
        error_messages={
            'invalid': "手机号格式错误"
        }
    )

    date_joined = serializers.DateTimeField(read_only=True)
    avatar = AvatarField(many=False, read_only=True)

    class Meta:
        fields = ("id", "username", "nickname", "avatar", "email", "phone", "date_joined")
        model = User


class UserRegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        max_length=15,
        allow_blank=False,
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all(), message="用户名已存在")],
        error_messages={
            "blank": "用户名不能为空",
            "max_length": "用户名不能超过15个字",
        }
    )

    password = serializers.CharField(
        allow_blank=False,
        required=True,
        write_only=True,
        error_messages={
            "blank": "密码不能为空"
        }
    )

    nickname = serializers.CharField(
        max_length=15,
        allow_blank=False,
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all(), message="昵称已存在")],
        error_messages={
            "blank": "昵称不能为空",
            "max_length": "昵称不能超过15个字",
        }
    )

    email = serializers.EmailField(
        required=False,
        allow_blank=True,
        error_messages={
            'invalid': "邮箱格式错误"
        }
    )

    phone = serializers.RegexField(
        regex=re.compile(r"^1(3\d|4[5-9]|5[0-35-9]|6[2567]|7[0-8]|8\d|9[0-35-9])\d{8}$"),
        required=False,
        allow_blank=True,
        error_messages={
            'invalid': "手机号格式错误"
        }
    )

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            nickname=validated_data['nickname'],
            email=validated_data.get('email', ""),
            phone=validated_data.get('phone', ""),
        )

        user.set_password(validated_data['password'])
        user.save()

        return user

    class Meta:
        fields = ("username", "password", "nickname", "email", "phone")
        model = User


class UserLoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ("username", "password")


class UserAvatarUploadView(APIView):
    parser_classes = (MultiPartParser,)
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        file = request.FILES.get("file")
        if file is None:
            return Result.err(msg="文件为空", code=400)
        suffix = file.name.split(".")[-1]
        allowed_suffixes = ["png", "jpg", "jpeg", "gif", "webp"]
        if suffix not in allowed_suffixes:
            return Result.err(msg="不支持此文件格式", code=400)
        new_filename = uuid.uuid4()
        full_filename = f"cattleya/avatar/{new_filename}.{suffix}"

        auth = oss2.Auth(settings.OSS_ACCESS_KEY_ID, settings.OSS_ACCESS_KEY_SECRET)
        bucket = oss2.Bucket(auth, settings.OSS_ENDPOINT, settings.OSS_BUCKET_NAME)
        if request.user.avatar is not None:
            bucket.delete_object(request.user.avatar)
        style = "image/crop,g_center,w_640,h_640,x_-320,y_-320"
        process = "{0}|sys/saveas,o_{1},b_{2}".format(style,
                                                      oss2.compat.to_string(base64.urlsafe_b64encode(
                                                          oss2.compat.to_bytes(full_filename))),
                                                      oss2.compat.to_string(base64.urlsafe_b64encode(
                                                          oss2.compat.to_bytes(settings.OSS_BUCKET_NAME))))
        bucket.put_object(full_filename, file)
        bucket.process_object(full_filename, process)
        request.user.avatar = full_filename
        request.user.save()
        return Result.ok(code=201, msg="上传成功")


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    authentication_classes = (TokenAuthentication,)
    permissions_classes_by_action = {
        "list": (IsAdminUser,),
        "retrieve": (IsAuthenticated,),
        "update": (IsAdminUser,),
        "partial_update": (IsOwner,),
        "destroy": (IsAdminUser,),
        "create": (AllowAny,),
        "whoami": (IsAuthenticated,),
        "change_password": (IsAuthenticated,),
    }

    def get_permissions(self):
        try:
            return [permission() for permission in self.permissions_classes_by_action[self.action]]
        except KeyError:
            return [permission() for permission in self.permission_classes]

    def get_serializer_class(self):
        if self.action == "create":
            self.serializer_class = UserRegisterSerializer
        else:
            self.serializer_class = UserSerializer
        return self.serializer_class

    @action(detail=False, methods=["get"])
    def whoami(self, request):
        return Result.ok(code=200, data=request.user.id)

    @action(detail=False, methods=["post"])
    def change_password(self, request: Request):
        old_password = request.data.get("old_password", "")
        new_password = request.data.get("new_password", None)
        if new_password is None or new_password == "":
            raise serializers.ValidationError("新密码不能为空")
        user = authenticate(username=request.user.username, password=old_password)
        if user is None:
            raise serializers.ValidationError("旧密码错误")
        user.set_password(new_password)
        user.save()
        return Result.ok(msg="修改成功")


class UserLoginAPIView(APIView):
    serializer_class = UserLoginSerializer
    permission_classes = ()
    authentication_classes = (TokenAuthentication,)

    def post(self, request: Request):
        serializer = UserLoginSerializer(data=request.data)
        user = authenticate(username=serializer.initial_data['username'], password=serializer.initial_data['password'])
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({"code": 200, "token": token.key, "id": user.id, "msg": ["登录成功"]},
                            status=status.HTTP_200_OK)
        raise serializers.ValidationError("用户名或密码有误")


class UserLogoutAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def get(self, request: Request):
        Token.objects.filter(user=request.user).delete()
        return Result.ok(msg="拜拜")
