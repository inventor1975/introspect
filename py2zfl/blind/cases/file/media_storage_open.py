from django.core.exceptions import SuspiciousFileOperation
from django.core.files.storage import FileSystemStorage
from django.http import FileResponse, Http404

scans = FileSystemStorage(location="/srv/app/scans")


def scan_file(request):
    name = request.GET.get("name", "")
    try:
        if not scans.exists(name):
            raise Http404("scan not found")
        handle = scans.open(name, "rb")
    except SuspiciousFileOperation:
        raise Http404("scan not found")
    return FileResponse(handle, as_attachment=True)
