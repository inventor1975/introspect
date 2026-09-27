from pathlib import Path

from django.http import FileResponse, Http404
from django.urls import path

MEDIA_ROOT = Path("/srv/cms/media")


def serve_media(request, relpath):
    target = MEDIA_ROOT / relpath
    if not target.is_file():
        raise Http404("not found")
    return FileResponse(target.open("rb"))


urlpatterns = [
    path("media/<path:relpath>", serve_media),
]
