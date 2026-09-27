import os

from django.http import Http404, HttpResponse
from django.views import View


class LegalPageView(View):
    root = "/srv/site/legal"
    pages = frozenset({"terms.html", "privacy.html", "cookies.html", "imprint.html"})

    def resolve(self, name):
        if name not in self.pages:
            raise Http404("unknown page")
        return os.path.join(self.root, name)

    def get(self, request):
        page = request.GET.get("page", "terms.html")
        with open(self.resolve(page), encoding="utf-8") as fh:
            return HttpResponse(fh.read())
