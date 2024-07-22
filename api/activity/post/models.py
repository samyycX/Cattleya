from django.core.serializers.json import DjangoJSONEncoder
from django.db import models
from django.db.models import QuerySet
from django.forms import model_to_dict
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets, serializers, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.request import Request
from rest_framework.response import Response

from api.models import User
from api.utils.emoticon import Emoticon
from api.utils.result import Result


class ActivityPostManager(models.Manager):

    def query_reverse_batch(self, start: int, amount: int):
        count = super().get_queryset().count()
        result = list(
            map(model_to_dict, super().get_queryset().filter(id__range=(count - start - amount + 1, count - start))))
        result.reverse()
        return result


class ActivityPost(models.Model):
    id = models.AutoField(primary_key=True, blank=False, null=False, unique=True)
    author = models.ForeignKey(User, verbose_name="发布作者", on_delete=models.DO_NOTHING,
                               related_name="re_activity_author")
    content = models.TextField(verbose_name="内容")
    time = models.DateTimeField(verbose_name="发布时间", auto_now=True)
    likes = models.ManyToManyField(User, verbose_name="点赞", related_name="re_activity_likes", default=[])
    objects = ActivityPostManager()

    class Meta:
        verbose_name = "动态帖子"


class ActivityPostCreateSerializer(serializers.ModelSerializer):
    content = serializers.CharField(
        max_length=300,
        allow_blank=False,
        allow_null=False,
        required=True,
        error_messages={
            "blank": "内容不能为空",
            "max_length": "内容不能超过{max_length}个字"
        })

    class Meta:
        model = ActivityPost
        fields = ('content',)


class ActivityPostSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    author = serializers.PrimaryKeyRelatedField(many=False, read_only=True)
    content = serializers.CharField(read_only=True)
    time = serializers.DateTimeField(read_only=True)
    likes = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = ActivityPost
        fields = ('id', 'author', 'content', 'time', 'likes')


class ActivityPostViewSet(viewsets.ModelViewSet):
    model = ActivityPost
    queryset = ActivityPost.objects.order_by("-id")
    authentication_classes = (TokenAuthentication,)
    permissions_classes_by_action = {
        "list": (IsAuthenticated,),
        "retrieve": (IsAuthenticated,),
        "update": (IsAdminUser,),
        "partial_update": (IsAdminUser,),
        "destroy": (IsAdminUser,),
        "create": (IsAuthenticated,),
        "like": (IsAuthenticated,),
    }

    def get_permissions(self):
        try:
            return [permission() for permission in self.permissions_classes_by_action[self.action]]
        except KeyError:
            return [permission() for permission in self.permission_classes]

    def get_serializer_class(self):
        if self.action == 'create':
            self.serializer_class = ActivityPostCreateSerializer
        else:
            self.serializer_class = ActivityPostSerializer
        return self.serializer_class

    def create(self, request):
        serializer = ActivityPostCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        content = serializer.validated_data['content']
        post = ActivityPost.objects.create(
            author=request.user,
            content=content,
        )
        post.save()

        return Result.ok(code=201, msg="发布成功")

    @action(detail=True, methods=["post"])
    def like(self, request: Request, pk=None):
        post = self.get_object()
        liked = False
        try:
            post.likes.get(id=request.user.id)
            post.likes.remove(request.user)
        except User.DoesNotExist:
            liked = True
            post.likes.add(request.user)

        return Result.ok(msg="点赞成功" if liked else "取消点赞成功", data=liked)
