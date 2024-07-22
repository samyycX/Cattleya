import os.path
import re

from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from django.core.files import File
from django.db.models import QuerySet
from django.http import JsonResponse
from django.http.request import HttpRequest
from django.contrib.auth import authenticate, login, logout
from api.decorator.viewdecorator import api_controller, file_filter
from .models import User, Avatar
import uuid

from ..utils.result import Result

# Create your views here.

EMAIL_REGEX = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")
PHONE_REGEX = re.compile(r"^1(3\d|4[5-9]|5[0-35-9]|6[2567]|7[0-8]|8\d|9[0-35-9])\d{8}$")


@api_controller
def user_register(request: HttpRequest):
    username = request.POST.get('username', '')
    if User.objects.filter(username=username):
        return Result.err(403, '用户已存在')

    password = request.POST.get('password', '')

    if password == '':
        return Result.err(403, '密码不能为空')

    email = request.POST.get('email', '')

    if email != "" and EMAIL_REGEX.match(email) is None:
        return Result.err(403, "邮箱格式错误")

    phone = request.POST.get('phone', '')

    if phone != "" and PHONE_REGEX.match(phone) is None:
        return Result.err(403, "手机号格式错误")

    User.objects.create_user(
        username=username,
        nickname=username,
        password=password,
        email=email,
        phone=phone,
        is_active=0,
        is_superuser=0
    )

    return Result.success("注册成功")


@api_controller
def user_login(request: HttpRequest):
    username = request.POST.get("username", "")
    password = request.POST.get("password", "")

    if not User.objects.filter(username=username):
        return Result.err(403, "用户名不存在")

    user = authenticate(username=username, password=password)

    if not user:
        return Result.err(403, "密码错误")

    if not user.is_active:
        return Result.err(403, "用户未激活")

    login(request, user)
    return JsonResponse({
        'code': 200,
        'msg': '登录成功'
    })


@api_controller
def user_logout(request: HttpRequest):
    logout(request)
    return Result.success("退出登录成功")


# TODO: 修改重定向URL
@login_required
@api_controller(methods=["POST", "GET"])
def user_info(request: HttpRequest):
    IMMUTABLE_FIELDS = ["username", "password", "registered_time"]
    user = request.user
    if request.method == "POST":
        for key, value in request.POST.items():
            if key in IMMUTABLE_FIELDS:
                continue
            if value is None:
                continue
            if hasattr(user, key):
                if key == "email" and value != "" and EMAIL_REGEX.match(value) is None:
                    return Result.err(403, "邮箱格式错误")
                if key == "phone" and value != "" and PHONE_REGEX.match(value) is None:
                    return Result.err(403, "手机号格式错误")
                if key == "nickname" and len(value) == 0 or len(value) > 15:
                    return Result.err(403, "昵称不合法")
                setattr(user, key, value)

        user.save()
        return Result.success("修改成功")
    elif request.method == "GET":
        user_id = request.GET.get("id", None)
        username = request.GET.get("username", None)

        try:
            if user_id is not None:
                user = User.objects.get(id=user_id)
            if username is not None:
                user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Result.err(404, "未找到该用户")

        return Result.success(
            data={
                "id": user.id,
                "username": user.username,
                "nickname": user.nickname,
                "email": user.email,
                "phone": user.phone,
                "registered_time": user.registered_time
            }
        )


@login_required
@api_controller
def user_change_password(request: HttpRequest):
    user = request.user
    old_password, new_password = request.POST.get("oldPassword", ""), request.POST.get("newPassword", None)

    if not new_password:
        return Result.err(400, "请求错误")
    if not check_password(old_password, user.password):
        return Result.err(403, "密码错误")

    user.set_password(new_password)
    user.save()
    return Result.success("修改成功")


@login_required
@api_controller(methods=["GET", "POST"], fix_post=False)
@file_filter(strategy="IMAGE")
def user_avatar(request: HttpRequest):
    if request.method == "POST":
        file: File = request.FILES.get('file', None)
        if file is None:
            return Result.err(400, "文件上传错误")
        existed: QuerySet = Avatar.objects.filter(user=request.user)
        if existed.exists():
            existed.delete()

        avatar = Avatar(user=request.user, image=file)
        avatar.save()
        return Result.success("上传成功")
    elif request.method == "GET":
        username = request.GET.get("username", request.user.username)

        try:
            user = User.objects.get(username=username)

            avatar = Avatar.objects.filter(user=user)
            if not avatar.exists():
                return Result.success()

            return Result.success(data=avatar.first().get_temporary_link())
        except User.DoesNotExist:
            return Result.err(400, "请求参数错误")
