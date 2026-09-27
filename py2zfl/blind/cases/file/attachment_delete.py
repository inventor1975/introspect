import os

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST

ATTACHMENT_DIR = settings.MEDIA_ROOT / "attachments"


@login_required
@require_POST
def delete_attachment(request):
    rel_path = request.POST["path"]
    target = os.path.join(ATTACHMENT_DIR, request.user.username, rel_path)
    if os.path.exists(target):
        os.remove(target)
        return JsonResponse({"deleted": rel_path})
    return JsonResponse({"error": "not found"}, status=404)
