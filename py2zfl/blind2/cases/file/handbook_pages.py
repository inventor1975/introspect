import re

from django.http import Http404, HttpResponse, HttpResponseBadRequest

HANDBOOK_DIR = "/srv/handbook/markdown"
SLUG_RE = re.compile(r"[A-Za-z0-9_-]+")


def handbook_page(request):
    slug = request.GET.get("page", "welcome")
    if not SLUG_RE.match(slug):
        return HttpResponseBadRequest("bad page name")
    try:
        with open(f"{HANDBOOK_DIR}/{slug}.md", encoding="utf-8") as fh:
            content = fh.read()
    except FileNotFoundError:
        raise Http404(slug)
    return HttpResponse(content, content_type="text/markdown; charset=utf-8")
