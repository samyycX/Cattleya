from datetime import datetime

from django.db import models
from django.db.models import QuerySet
from rest_framework import serializers, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated, BasePermission, IsAdminUser, AllowAny
from rest_framework.request import Request
from rest_framework.validators import UniqueValidator

from api.models import User, UserBriefSerializer
from api.renderer import JSONResponseRenderer
from api.utils.result import Result


class CanWriteBlog(BasePermission):
    def has_permission(self, request, view):
        return IsAdminUser().has_permission(request, view) or bool(
            request.user and request.user.has_perm("api.blog"))


class IsBlogOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return CanWriteBlog().has_permission(request, view) and obj.author.id == request.user.id


class BlogTag(models.Model):
    id = models.AutoField(primary_key=True, blank=False, null=False, unique=True)
    name = models.CharField(verbose_name="标签名称", max_length=64, unique=True)
    created_time = models.DateTimeField(verbose_name="创建时间", auto_now=True)

    @property
    def count(self):
        return Blog.objects.filter(tags__id__contains=self.id).count()


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
        fields = ("name",)


class BlogTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogTag
        fields = ("id", "name", "count", "created_time")


class BlogTagViewSet(viewsets.ModelViewSet):
    queryset = BlogTag.objects.all()
    authentication_classes = (TokenAuthentication,)
    pagination_class = None
    renderer_classes = (JSONResponseRenderer,)
    permissions_classes_by_action = {
        "list": (AllowAny,),
        "retrieve": (AllowAny,),
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
    visible = models.BooleanField(verbose_name="可见性")
    created_time = models.DateTimeField(verbose_name="发布时间", auto_now_add=True)
    updated_time = models.DateTimeField(verbose_name="最后一次更新时间", auto_now_add=True)
    # TODO: 添加以下数据链接
    tags = models.ManyToManyField(BlogTag, verbose_name="标签")

    # comments = models.ForeignKey(BlogComment, verbose_name="评论")

    @property
    def length(self):
        return len(self.content)

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
        fields = ('id', 'author', 'title', 'content', 'visible', 'tags', 'created_time', 'updated_time')
        read_only_fields = ('id', 'author', 'created_time', 'uploaded_time')


class BlogSerializer(serializers.ModelSerializer):
    author = UserBriefSerializer(read_only=True)
    tags = BlogTagSerializer(many=True)

    class Meta:
        model = Blog
        fields = ('id', 'author', 'title', 'content', 'visible', 'created_time', 'updated_time', 'tags', 'length')
        read_only_fields = ('id', 'author', 'created_time', 'updated_time', 'length')

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.content = validated_data.get('content', instance.content)
        instance.visible = validated_data.get('visible', instance.visible)
        if 'tags' in validated_data:
            instance.tags.set(validated_data['tags'])
        instance.updated_time = datetime.now()
        instance.save()
        return instance


class BlogBriefSerializer(serializers.ModelSerializer):
    author = UserBriefSerializer(read_only=True)
    tags = BlogTagSerializer(many=True, read_only=True)

    class Meta:
        model = Blog
        fields = ("id", "author", "title", "length", "created_time", "updated_time", "tags", "visible")


class BlogViewSet(viewsets.ModelViewSet):
    model = Blog,
    queryset = Blog.objects.all()
    authentication_classes = (TokenAuthentication,)
    renderer_classes = (JSONResponseRenderer,)
    permissions_classes_by_action = {
        "list": (AllowAny,),
        "retrieve": (AllowAny,),
        "update": (IsBlogOwner,),
        "partial_update": (IsBlogOwner,),
        "destroy": (IsBlogOwner,),
        "create": (CanWriteBlog,),
        "list_brief_by_latest": (AllowAny,),
        "brief": (AllowAny,),
    }
    serializers_class_by_action = {
        "create": BlogCreateSerializer,
        "update": BlogCreateSerializer,
        "partial_update": BlogCreateSerializer,
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
        visible = query_params.get("visible", "true")

        result = Blog.objects.all().order_by('-created_time')

        if tag is not None:
            try:
                tag = BlogTag.objects.get(id=tag)
                result = result.filter(tags__id__contains=tag.id)
            except BlogTag.DoesNotExist:
                raise serializers.ValidationError("标签不存在")

        if visible == "false":
            if not IsAdminUser().has_permission(self.request, None):
                raise serializers.ValidationError("无权限")
            result = result.filter(visible=False)
        elif visible == "all":
            if not IsAdminUser().has_permission(self.request, None):
                raise serializers.ValidationError("无权限")
        else:
            result = result.filter(visible=True)

        return result

    def create(self, request, *args, **kwargs):
        serializer = BlogCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        blog = Blog.objects.create(
            author=request.user,
            title=serializer.validated_data['title'],
            content=serializer.validated_data['content'],
            visible=serializer.validated_data['visible']
        )
        blog.tags.set(serializer.validated_data['tags'])
        return Result.ok(code=200, data=BlogSerializer(blog).data)

    @action(detail=False, methods=["get"])
    def listBriefByLatest(self, request: Request, pk=None):
        queryset = self.get_queryset().order_by('-created_time')
        page = self.paginate_queryset(queryset)
        if page is not None:
            return self.get_paginated_response(BlogBriefSerializer(page, many=True).data)

        return Result.ok(code=200, data={"next": None, "results": BlogBriefSerializer(queryset, many=True).data})

    @action(detail=True, methods=["get"])
    def brief(self, request: Request, pk=None):
        blog = self.get_object()
        blog_brief_data = BlogBriefSerializer(blog).data
        return Result.ok(code=200, data=blog_brief_data)

    def partial_update(self, request: Request, *args, **kwargs):
        result = super().partial_update(request, *args, **kwargs)
        if "title" in request.data or "content" in request.data:
            blog = self.get_object()
            blog.updated_time = datetime.utcnow()
            blog.save()
        return result
