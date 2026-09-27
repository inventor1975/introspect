import os

from django.conf import settings
from django.http import FileResponse, Http404

FONT_DIR = os.path.join(settings.STATIC_ROOT, "fonts")


def font_file(request):
    requested = request.GET.get("font", "")
    available = set(os.listdir(FONT_DIR))
    if requested not in available:
        raise Http404("font not available")
    return FileResponse(open(os.path.join(FONT_DIR, requested), "rb"), content_type="font/woff2")
