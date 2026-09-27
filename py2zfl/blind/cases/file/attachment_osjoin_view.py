import os

from django.conf import settings
from django.core.exceptions import SuspiciousFileOperation
from django.http import FileResponse, Http404
from django.utils._os import safe_join


def attachment(request):
    name = request.GET.get("name", "")
    try:
        path = safe_join(settings.MEDIA_ROOT, "attachments", name)
    except SuspiciousFileOperation:
        raise Http404("invalid attachment")
    if not os.path.isfile(path):
        raise Http404("missing attachment")
    return FileResponse(open(path, "rb"), as_attachment=True)
