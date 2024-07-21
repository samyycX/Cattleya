from django.contrib.auth.decorators import login_required
from django.forms import model_to_dict
from django.http import HttpRequest

from api.activity.post.models import ActivityPost
from api.decorator.viewdecorator import api_controller
from api.utils.result import Result


@api_controller(methods=["GET", "POST"])
@login_required
def activity_post(request: HttpRequest):
    if request.method == "GET":
        try:
            post_id = request.GET.get("id", None)[0]
            post = ActivityPost.objects.get(id=post_id)
            return Result.success(data=model_to_dict(post))
        except TypeError:
            return Result.err(403, "请求参数错误")
        except ActivityPost.DoesNotExist:
            return Result.err(404, "未找到该帖子")

    elif request.method == "POST":
        content = request.POST.get("content", None)
        if content is None or content == "":
            return Result.err(403, "内容不能为空")
        post = ActivityPost.objects.create(author=request.user, content=content)

        return Result.success("上传成功")


@api_controller(methods=["GET"])
@login_required
def activity_posts(request: HttpRequest):
    try:
        start = int(request.GET.get("start", 0))
        amount = int(request.GET.get("amount", 10))
    except ValueError:
        return Result.err(403, "参数类型非法")
    if amount <= 0 or amount >= 50:
        return Result.err(403, "amount 参数非法")

    return Result.success(data=ActivityPost.objects.query_reverse_batch(start, amount))
