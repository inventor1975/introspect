import os

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import FileResponse, Http404

INVOICE_ROOT = os.path.join(settings.MEDIA_ROOT, "invoices")


@login_required
def invoice_pdf(request):
    filename = request.GET.get("file", "")
    if not filename.endswith(".pdf"):
        raise Http404("Unknown invoice")
    full_path = os.path.join(INVOICE_ROOT, filename)
    try:
        handle = open(full_path, "rb")
    except FileNotFoundError:
        raise Http404("Unknown invoice")
    return FileResponse(handle, content_type="application/pdf")
