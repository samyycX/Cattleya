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