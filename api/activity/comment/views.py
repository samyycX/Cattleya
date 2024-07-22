from django.contrib.auth.decorators import login_required
from django.forms import model_to_dict
from django.http import HttpRequest

from api.activity.comment.models import ActivityComment
from api.activity.post.models import ActivityPost
from api.decorator.viewdecorator import api_controller
from api.utils.result import Result


@api_controller(methods=["GET", "POST"])
@login_required
def activity_comment(request: HttpRequest):
    if request.method == "GET":
        comment_ids = request.GET.get("id", None)
        comment_owner = request.GET.get("owner", None)
        if comment_ids is not None:
            return Result.success(data=list(ActivityComment.objects.filter(id__in=comment_ids).values()))
        if comment_owner is not None:
            comment_owner = comment_owner[0]
            return Result.success(data=list(ActivityComment.objects.filter(owner=comment_owner).values()))
        return Result.err(403, "请求参数不合法")
    elif request.method == "POST":
        content = request.POST.get("content", None)
        father_comment = request.POST.get("fatherComment", None)
        owner = request.POST.get("owner", None)

        if content is None or owner is None:
            return Result.err(403, "请求参数不合法")

        if father_comment is not None:
            try:
                father_comment = ActivityComment.objects.get(id=father_comment)
                if father_comment.father_comment is not None:
                    return Result.err(403, "暂时禁止回复子评论")
                if father_comment.owner != owner:
                    return Result.err(403, "...你是怎么发出这样的回复的？")
            except ActivityComment.DoesNotExist:
                return Result.err(403, "原回复不见了")

        try:
            owner = ActivityPost.objects.get(id=owner)
        except ActivityPost.DoesNotExist:
            return Result.err(403, "原始帖子已消失")

        ActivityComment.objects.create(author=request.user, content=content, father_comment=father_comment, owner=owner)

        return Result.success("评论成功")