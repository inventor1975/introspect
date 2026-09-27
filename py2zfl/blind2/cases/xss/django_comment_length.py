from django.http import HttpResponse
from django.views.decorators.http import require_POST

MAX_LEN = 500


@require_POST
def comment_check(request):
    comment = request.POST.get("comment", "")
    used = len(comment)
    remaining = MAX_LEN - used
    state = "over" if remaining < 0 else "ok"
    return HttpResponse(
        f"<p class='counter counter-{state}'>{used} characters used, {remaining} left</p>"
    )
