from datetime import datetime

from django.http import HttpRequest, HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from api.activity.health.models import Health
from api.decorator.viewdecorator import api_controller
from cattleya import settings


@api_controller(methods=["GET", "POST"])
@csrf_exempt
def health_view(request: HttpRequest):
    if Health.objects.all().count() == 0:
        health = Health.objects.create(last_heartrate=-1, last_updated_time=datetime.now())
    else:
        health = Health.objects.get(id=1)

    if request.method == "GET":
        return JsonResponse({
            "code": 200,
            "last_heartrate": health.last_heartrate,
            "last_updated_time": health.last_updated_time
        })
    elif request.method == "POST":
        if "Secret" not in request.headers or request.headers.get("Secret") != settings.HEALTH_SECRET:
            return HttpResponse(400)

        for data in request.POST["data"]["metrics"]:
            if data['name'] == 'heart_rate':
                heartrate_data = data['data'][-1]
                health.last_heartrate = heartrate_data["Avg"]
                health.last_updated_time = heartrate_data["date"]
                health.save()

        return JsonResponse({"code": 200})
