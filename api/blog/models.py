from django.db import models
from django.db.models import QuerySet
from rest_framework import serializers, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated, BasePermission, IsAdminUser, AllowAny
from rest_framework.request import Request
from rest_framework.validators import UniqueValidator

from api.models import User


class CanWriteBlog(BasePermission):
    def has_permission(self, request, view):
        return IsAdminUser().has_permission(self, request, view) or bool(
            request.user and request.user.has_perm("api.blog"))


class IsBlogOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return CanWriteBlog().has_permission(self, request, view) and obj.author == request.user.id


class BlogTag(models.Model):
    id = models.AutoField(primary_key=True, blank=True, null=True, unique=True)
    name = models.CharField(verbose_name="标签名称", max_length=64, unique=True)
    created_time = models.DateTimeField(verbose_name="创建时间", auto_now=True)


class BlogTagCreateSerializer(serializers.ModelSerializer):
    name = serializers.CharField(
        required=True,
        allow_blank=False,
        allow_null=False,
        max_length=64,
        validators=[UniqueValidator(queryset=BlogTag.objects.all(), message="标签已存在")],
        error_messages={
            "blank": "标签不能为空",
            "max_length": "标签不能超过{max_length}个字"
        }
    )

    class Meta:
        model = BlogTag


class BlogTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogTag
        fields = ("id", "name", "created_time")


class BlogTagViewSet(viewsets.ModelViewSet):
    queryset = BlogTag.objects.all()
    authentication_classes = (TokenAuthentication,)
    permissions_classes_by_action = {
        "list": (AllowAny,),
        "retrieve": (IsAuthenticated,),
        "update": (IsAdminUser,),
        "partial_update": (IsAdminUser,),
        "destroy": (IsAdminUser,),
        "create": (CanWriteBlog,),
    }
    serializers_class_by_action = {
        "create": BlogTagCreateSerializer,
        "*": BlogTagSerializer
    }

    def get_permissions(self):
        try:
            return [permission() for permission in self.permissions_classes_by_action[self.action]]
        except KeyError:
            return [permission() for permission in self.permission_classes]

    def get_serializer_class(self):
        if self.action in self.serializers_class_by_action:
            return self.serializers_class_by_action[self.action]
        return self.serializers_class_by_action["*"]


class Blog(models.Model):
    id = models.AutoField(primary_key=True, blank=False, null=False, unique=True)
    author = models.ForeignKey(User, verbose_name="作者", on_delete=models.DO_NOTHING)
    title = models.TextField(verbose_name="标题", max_length=255)
    content = models.TextField(verbose_name="内容", max_length=16777215)
    created_time = models.DateTimeField(verbose_name="发布时间", auto_now=True)
    updated_time = models.DateTimeField(verbose_name="最后一次更新时间", auto_now=True)
    # TODO: 添加以下数据链接
    tags = models.ManyToManyField(BlogTag, verbose_name="标签")

    # comments = models.ForeignKey(BlogComment, verbose_name="评论")

    class Meta:
        permissions = [
            ("blog", "Can control blog.")
        ]


class BlogCreateSerializer(serializers.ModelSerializer):
    title = serializers.CharField(
        max_length=255,
        allow_blank=False,
        allow_null=False,
        required=True,
        error_messages={
            "blank": "回复不能为空",
            "max_length": "标题不能超过{max_length}个字"
        }
    )

    content = serializers.CharField(
        max_length=16777215,
        allow_blank=False,
        allow_null=False,
        required=True,
        error_messages={
            "blank": "内容不能为空",
            "max_length": "内容不能超过{max_length}个字"
        }
    )

    tags = serializers.PrimaryKeyRelatedField(
        required=False,
        many=True,
        queryset=BlogTag.objects.all(),
        error_messages={
            'does_not_exist': '标签pk={pk_value}不存在'
        }
    )

    class Meta:
        model = Blog
        fields = ('title', 'content', 'tags')


class BlogSerializer(serializers.ModelSerializer):
    tags = serializers.StringRelatedField(
        many=True,
        queryset=BlogTag.objects.all()
    )

    class Meta:
        model = Blog
        fields = ('id', 'author', 'title', 'content', 'created_time', 'uploaded_time', 'tags')


class BlogViewSet(viewsets.ModelViewSet):
    model = Blog,
    queryset = Blog.objects.all()
    authentication_classes = (TokenAuthentication,)
    permissions_classes_by_action = {
        "list": (AllowAny,),
        "retrieve": (AllowAny,),
        "update": (IsBlogOwner,),
        "partial_update": (IsBlogOwner,),
        "destroy": (IsBlogOwner,),
        "create": (CanWriteBlog,),
    }
    serializers_class_by_action = {
        "create": BlogCreateSerializer,
        "*": BlogSerializer
    }

    def get_permissions(self):
        try:
            return [permission() for permission in self.permissions_classes_by_action[self.action]]
        except KeyError:
            return [permission() for permission in self.permission_classes]

    def get_serializer_class(self):
        if self.action in self.serializers_class_by_action:
            return self.serializers_class_by_action[self.action]
        return self.serializers_class_by_action["*"]

    def get_queryset(self):
        query_params = self.request.query_params
        tag = query_params.get("tag", None)

        if tag is not None:
            try:
                tag = BlogTag.objects.get(id=tag)
                return Blog.objects.filter(tag=tag)
            except BlogTag.DoesNotExist:
                raise serializers.ValidationError("标签不存在")

        return Blog.objects.all()
