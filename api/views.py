from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.exceptions import ErrorDetail

from cattleya import settings
from .user.views import *
from .activity.views import *

from rest_framework.views import exception_handler

from api.utils.emoticon import Emoticon


def my_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:

        msg = []
        if isinstance(response.data, dict):
            for data_key, item in response.data.items():
                if isinstance(item, ErrorDetail):
                    msg.append(f"{data_key}: {item.title()}")
                elif isinstance(item, list) and hasattr(item[0], "title"):
                    msg.append(f"{data_key}: {item[0].title()}")
        if isinstance(response.data, list):
            for item in response.data:
                if isinstance(item, ErrorDetail):
                    if hasattr(item, "title"):
                        msg.append(f"{item.title()}")

        response.data = {"msg": msg, "code": response.status_code}
        response.status_code = 200
    return response
