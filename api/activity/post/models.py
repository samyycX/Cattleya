from django.contrib.auth.models import User
from django.db import models
from django.db.models import QuerySet


class ActivityPostManager(models.Manager):

    def query_reverse_batch(self, start: int, amount: int):
        count = super().get_queryset().count()
        return list(reversed(super().get_queryset().filter(id__range=(count - start - amount + 1, count - start)).values()))


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