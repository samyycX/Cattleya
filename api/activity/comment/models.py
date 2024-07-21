from django.contrib.auth.models import User
from django.db import models

from api.activity.post.models import ActivityPost

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
