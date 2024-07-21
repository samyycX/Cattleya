# Generated by Django 4.2.13 on 2024-07-19 09:18

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api', '0003_userprofile_nickname'),
    ]

    operations = [
        migrations.RenameField(
            model_name='activitycomment',
            old_name='fatherComment',
            new_name='father_comment',
        ),
        migrations.AlterField(
            model_name='activitypost',
            name='likes',
            field=models.ManyToManyField(default=[], related_name='re_activity_likes', to=settings.AUTH_USER_MODEL, verbose_name='点赞'),
        ),
    ]
