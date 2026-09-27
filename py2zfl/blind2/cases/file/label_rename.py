import os
import re

from django.http import HttpResponseBadRequest, JsonResponse
from django.views.decorators.http import require_POST

LABEL_DIR = "/srv/printing/labels"
LABEL_NAME = re.compile(r"[A-Za-z0-9_-]{1,40}\.zpl")


@require_POST
def rename_label(request):
    current = request.POST.get("current", "")
    desired = request.POST.get("desired", "")
    for value in (current, desired):
        if not LABEL_NAME.fullmatch(value):
            return HttpResponseBadRequest(f"invalid label name: {value}")
    os.replace(os.path.join(LABEL_DIR, current), os.path.join(LABEL_DIR, desired))
    return JsonResponse({"label": desired})
