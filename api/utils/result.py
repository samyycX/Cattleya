from django.http import JsonResponse
from typing import *

from rest_framework.response import Response

from api.utils.emoticon import Emoticon


class Result:
    @staticmethod
    def err(code: int, msg: Optional[str] = None):
        return Response({
            'code': code,
            'msg': [Emoticon.success(msg)]
        })

    @staticmethod
    def success(msg: Optional[str] = None, data: Optional[Any] = None):
        return JsonResponse({
            'code': 200,
            'msg': Emoticon.success(msg),
            'data': data
        })

    @staticmethod
    def ok(*, code: Optional[int] = 200, msg: Optional[str] = None, data: Optional[Any] = None):
        return Response({
            'code': code,
            'msg': [Emoticon.success(msg)],
            'data': data
        })
