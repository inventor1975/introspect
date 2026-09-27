import hashlib
import os

import requests
from django.http import HttpResponse, HttpResponseBadRequest

CACHE_DIR = "/var/cache/link-previews"


def link_preview(request):
    url = request.GET.get("url", "")
    if not url.startswith(("http://", "https://")):
        return HttpResponseBadRequest("absolute URL required")
    key = hashlib.sha256(url.encode("utf-8")).hexdigest()
    cached = os.path.join(CACHE_DIR, key[:2], key + ".html")
    if os.path.exists(cached):
        with open(cached, "rb") as fh:
            return HttpResponse(fh.read(), content_type="text/html")
    body = requests.get("https://preview.internal/render", params={"u": url}, timeout=5).content
    os.makedirs(os.path.dirname(cached), exist_ok=True)
    with open(cached, "wb") as fh:
        fh.write(body)
    return HttpResponse(body, content_type="text/html")
