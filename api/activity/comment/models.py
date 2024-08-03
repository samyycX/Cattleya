from django.db import models
from rest_framework import serializers, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.request import Request

from api.activity.post.models import ActivityPost
from api.models import User
from api.utils.emoticon import Emoticon
from api.utils.result import Result


class ActivityCommentManager(models.Manager):
    pass


class ActivityComment(models.Model):
    id = models.AutoField(primary_key=True, blank=False, null=False, unique=True)
    author = models.ForeignKey(User, verbose_name="评论发布者", on_delete=models.DO_NOTHING,
                               related_name="re_activity_comment_author")
    content = models.TextField(verbose_name="评论内容", max_length=200)
    time = models.DateTimeField(verbose_name="发布时间", auto_now=True)
    father_comment = models.ForeignKey("self", verbose_name="父评论", null=True, on_delete=models.CASCADE,
                                       related_name="re_activity_comment")
    owner = models.ForeignKey(ActivityPost, verbose_name="所属的帖子", null=False, on_delete=models.CASCADE,
                              related_name="re_activity_comment_activity")

    objects = ActivityCommentManager()

    class Meta:
        verbose_name = "动态的评论"


class ActivityCommentCreateSerializer(serializers.ModelSerializer):
    content = serializers.CharField(
        max_length=200,
        allow_blank=False,
        allow_null=False,
        required=True,
        error_messages={
            "blank": Emoticon.err("回复内容不能为空"),
            "max_length": Emoticon.err("回复不能超过{max_length}个字")
        }
    ),
    father_comment = serializers.PrimaryKeyRelatedField(
        required=False,
        many=False,
        queryset=ActivityComment.objects.all(),
        error_messages={
            'required': '此字段是必须的',
            'does_not_exist': '此评论(pk={pk_value})不存在',
            'incorrect_type': '不正确的类型，需要pk，得到{data_type}',
        }
    ),
    owner = serializers.PrimaryKeyRelatedField(
        required=True,
        many=False,
        queryset=ActivityPost.objects.all(),
        error_messages={
            'required': '此字段是必须的',
            'does_not_exist': '此帖子(pk={pk_value})不存在',
            'incorrect_type': '不正确的类型，需要pk，得到{data_type}',
        }
    )

    def validate(self, data):
        if 'father_comment' not in data or data['father_comment'] is None:
            return data
        if data['father_comment'].owner != data['owner']:
            raise serializers.ValidationError("你是怎么发出这个请求的？")
        if data['father_comment'].father_comment is not None:
            raise serializers.ValidationError("暂时不支持回复子评论..你是怎么发出这个请求的？")

        return data

    class Meta:
        model = ActivityComment
        fields = ("content", "father_comment", "owner")


class ActivityCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityComment
        fields = ("id", "author", "content", "father_comment", "owner", "time")


class ActivityCommentViewSet(viewsets.ModelViewSet):
    model = ActivityComment
    queryset = ActivityComment.objects.all()
    authentication_classes = (TokenAuthentication,)
    pagination_class = None
    permissions_classes_by_action = {
        "list": (IsAdminUser,),
        "retrieve": (IsAuthenticated,),
        "update": (IsAdminUser,),
        "partial_update": (IsAdminUser,),
        "destroy": (IsAdminUser,),
        "create": (IsAuthenticated,),
        "list_by_owner": (IsAuthenticated,),
    }

    def get_permissions(self):
        try:
            return [permission() for permission in self.permissions_classes_by_action[self.action]]
        except KeyError:
            return [permission() for permission in self.permission_classes]

    def get_serializer_class(self):
        if self.action == 'create':
            self.serializer_class = ActivityCommentCreateSerializer
        else:
            self.serializer_class = ActivityCommentSerializer
        return self.serializer_class

    def create(self, request):
        serializer = ActivityCommentCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        content = serializer.validated_data['content']
        father_comment = serializer.validated_data.get('father_comment', None)
        owner = serializer.validated_data['owner']
        comment = ActivityComment.objects.create(
            author=request.user,
            content=content,
            father_comment=father_comment,
            owner=owner,
        )
        comment.save()

        return Result.ok(code=201, msg="评论成功", data=ActivityCommentSerializer(comment).data)

    @action(detail=False, methods=["get"])
    def list_by_owner(self, request: Request):
        owner = request.query_params.get("owner", None)
        if owner is None:
            return Result.err(code=400, msg="owner不存在")

        self.queryset = ActivityComment.objects.filter(owner=owner)
        return self.list(request)