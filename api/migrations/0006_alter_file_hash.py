# Generated by Django 4.2.13 on 2024-08-05 06:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_file_hash_file_name_alter_file_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='hash',
            field=models.CharField(max_length=256, unique=True, verbose_name='哈希'),
        ),
    ]
