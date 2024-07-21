from django.http import JsonResponse
from typing import *

from api.utils.emoticon import Emoticon


class Result:
    @staticmethod
    def err(code: int, msg: Optional[str] = None):
        return JsonResponse({
            'code': code,
            'msg': Emoticon.err(msg)
        })

    @staticmethod
    def success(msg: Optional[str] = None, data: Optional[Any] = None):
        return JsonResponse({
            'code': 200,
            'msg': Emoticon.success(msg),
            'data': data
        })
