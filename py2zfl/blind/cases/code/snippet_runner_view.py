import contextlib
import io

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST


@login_required
@require_POST
def run_snippet(request):
    code = request.POST["code"]
    namespace = {"user": request.user.username}
    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        exec(code, namespace)
    return JsonResponse({"output": out.getvalue()})
