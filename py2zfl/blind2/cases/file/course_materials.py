from django.core.exceptions import SuspiciousFileOperation
from django.http import FileResponse, Http404
from django.utils._os import safe_join

MATERIALS_ROOT = "/srv/lms/materials"


def course_material(request, course_code):
    requested = request.GET.get("file", "")
    try:
        path = safe_join(MATERIALS_ROOT, course_code, requested)
    except SuspiciousFileOperation:
        raise Http404("material not found")
    try:
        return FileResponse(open(path, "rb"))
    except (FileNotFoundError, IsADirectoryError):
        raise Http404("material not found")
