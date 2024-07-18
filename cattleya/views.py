import os

from django.http import HttpResponse


def favicon_view(request):
    return HttpResponse(open("./frontend/dist/favicon.ico", 'rb'), content_type="image/x-icon")
