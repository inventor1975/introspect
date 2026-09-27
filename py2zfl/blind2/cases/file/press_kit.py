from django.core.files.storage import FileSystemStorage
from django.core.exceptions import SuspiciousFileOperation
from django.http import FileResponse, Http404

press_storage = FileSystemStorage(location="/srv/marketing/press-kit")


def press_asset(request):
    name = request.GET.get("asset", "")
    try:
        if not press_storage.exists(name):
            raise Http404("unknown asset")
        handle = press_storage.open(name, "rb")
    except SuspiciousFileOperation:
        raise Http404("unknown asset")
    return FileResponse(handle, as_attachment=True)
