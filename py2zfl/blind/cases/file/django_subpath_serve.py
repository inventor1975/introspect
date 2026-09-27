import mimetypes
from pathlib import Path

from django.http import Http404, HttpResponse
from django.urls import path

BASE_DIR = Path(__file__).resolve().parent
PUBLIC_DIR = BASE_DIR / "public"


def serve_public(request, subpath):
    target = PUBLIC_DIR / subpath
    if not target.is_file():
        raise Http404("missing")
    content_type, _ = mimetypes.guess_type(str(target))
    return HttpResponse(target.read_bytes(), content_type=content_type or "application/octet-stream")


urlpatterns = [
    path("public/<path:subpath>", serve_public, name="serve-public"),
]
