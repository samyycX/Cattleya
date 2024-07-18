import os.path

import oss2
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
import cattleya.settings as settings
import base64


# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    phone = models.CharField(verbose_name="手机号", max_length=30)
    registered_time = models.DateTimeField(verbose_name="注册时间", auto_now=True)

    objects = models.Manager()

    class Meta:
        verbose_name = "用户附加个人资料"


class Avatar(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.FileField(verbose_name="头像文件", upload_to="cattleya/avatar", null=True, blank=True)

    objects = models.Manager()

    class Meta:
        verbose_name = "用户头像"

    def get_temporary_link(self) -> str:
        auth = oss2.Auth(settings.OSS_ACCESS_KEY_ID, settings.OSS_ACCESS_KEY_SECRET)
        bucket = oss2.Bucket(auth, settings.OSS_ENDPOINT, settings.OSS_BUCKET_NAME)
        url = bucket.sign_url(method='GET', key=self.image.name.replace("\\", "/"),
                              expires=settings.OSS_EXPIRATION_TIME, slash_safe=True)
        return url


@receiver(post_save, sender=Avatar)
def save_avatar_to_oss(sender, **kwargs):
    avatar = kwargs['instance']
    file = avatar.image
    file.name = file.name.replace("\\", "/")
    style = "image/crop,g_center,w_640,h_640,x_-320,y_-320"
    auth = oss2.Auth(settings.OSS_ACCESS_KEY_ID, settings.OSS_ACCESS_KEY_SECRET)
    bucket = oss2.Bucket(auth, settings.OSS_ENDPOINT, settings.OSS_BUCKET_NAME)
    process = "{0}|sys/saveas,o_{1},b_{2}".format(style,
                                                  oss2.compat.to_string(base64.urlsafe_b64encode(
                                                      oss2.compat.to_bytes(file.name))),
                                                  oss2.compat.to_string(base64.urlsafe_b64encode(
                                                      oss2.compat.to_bytes(settings.OSS_BUCKET_NAME))))
    bucket.process_object(file.name, process)


@receiver(post_delete, sender=Avatar)
def delete_avatar_in_oss(sender, **kwargs):
    avatar = kwargs['instance']
    file = avatar.image
    file.name = file.name.replace("\\", "/")

    auth = oss2.Auth(settings.OSS_ACCESS_KEY_ID, settings.OSS_ACCESS_KEY_SECRET)
    bucket = oss2.Bucket(auth, settings.OSS_ENDPOINT, settings.OSS_BUCKET_NAME)
    bucket.delete_object(file.name)
