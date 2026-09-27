import os
import uuid

from django.conf import settings
from django.http import FileResponse, Http404, HttpResponseBadRequest

RECEIPT_DIR = os.path.join(settings.MEDIA_ROOT, "receipts")


def receipt(request):
    raw = request.GET.get("id", "")
    try:
        receipt_id = uuid.UUID(raw)
    except ValueError:
        return HttpResponseBadRequest("invalid receipt id")
    path = os.path.join(RECEIPT_DIR, f"{receipt_id}.pdf")
    if not os.path.exists(path):
        raise Http404
    return FileResponse(open(path, "rb"), content_type="application/pdf")
