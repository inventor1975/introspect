import os

from django.http import FileResponse, Http404

ARCHIVE_ROOT = os.path.realpath("/srv/accounting/archive")


def archived_invoice(request):
    relative = request.GET.get("path", "")
    full_path = os.path.realpath(os.path.join(ARCHIVE_ROOT, relative))
    if os.path.commonpath([full_path, ARCHIVE_ROOT]) != ARCHIVE_ROOT:
        raise Http404("invoice not found")
    if not os.path.isfile(full_path):
        raise Http404("invoice not found")
    return FileResponse(open(full_path, "rb"), as_attachment=True)
