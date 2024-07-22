from .user.views import *
from .activity.views import *

from rest_framework.views import exception_handler

from api.utils.emoticon import Emoticon


def my_exception_handler(exc, context):
    print(1)
    response = exception_handler(exc, context)

    if response is not None:

        msg = []
        if isinstance(response.data, dict):
            for data_key, data_array in response.data.items():
                if not (isinstance(data_array, list) and len(data_array) < 2):
                    continue
                if hasattr(data_array[0], "title"):
                    msg.append(Emoticon.err(f"{data_key}: {data_array[0].title()}"))
        print(response.data)
        response.data.clear()
        response.data["msg"] = msg
        response.data["code"] = response.status_code
        response.status_code = 200
    return response
