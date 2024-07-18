import json
import os
from json import JSONDecodeError
from typing import Callable, Any, List, Union

from django.http import JsonResponse
from django.http.request import HttpRequest, QueryDict


def api_controller(function=None, *, methods=None, fix_post=True):
    if methods is None:
        methods = ["POST"]

    def decorator(view_controller_func):
        def wrapper(request: HttpRequest, *args, **kwargs):
            if request.method not in methods:
                return JsonResponse({
                    'code': 405,
                    'msg': '请求方式错误'
                })

            if request.method == "POST" and fix_post:
                try:
                    request.POST = json.loads(request.body)
                except JSONDecodeError:
                    pass
            return view_controller_func(request, *args, **kwargs)

        return wrapper

    if function:
        return decorator(function)
    return decorator


def file_filter(function=None, *, strategy: Union["IMAGE", "GENERAL"] = "GENERAL"):
    filter = {
        "IMAGE": lambda x: x.lower() in [".jpg", ".png", ".jpeg", ".bmp"],
        "GENERAL": lambda x: x.lower() not in [".php", ".js", ".css", ".html"]
    }[strategy]

    def decorator(func):
        def wrapper(request: HttpRequest, *args, **kwargs):
            files = request.FILES
            if len(files) == 0:
                return func(request, *args, **kwargs)

            for name, file in files.items():
                ext = os.path.splitext(file.name)[1]
                if not filter(ext):
                    return JsonResponse({
                        'code': 400,
                        'msg': '不支持的文件拓展名'
                    })
            return func(request, *args, **kwargs)

        return wrapper

    if function:
        return decorator(function)
    return decorator