import os

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest, JsonResponse
from django.views.decorators.http import require_POST

FILE_ROOT = "/srv/filemanager/data"


def _user_root(user):
    return os.path.join(FILE_ROOT, user.username)


@login_required
@require_POST
def rename_entry(request):
    old_name = request.POST.get("from")
    new_name = request.POST.get("to")
    if not old_name or not new_name:
        return HttpResponseBadRequest("from and to are required")
    root = _user_root(request.user)
    src = os.path.join(root, old_name)
    dst = os.path.join(root, new_name)
    if os.path.exists(dst):
        return JsonResponse({"error": "target exists"}, status=409)
    os.rename(src, dst)
    return JsonResponse({"renamed": [old_name, new_name]})
