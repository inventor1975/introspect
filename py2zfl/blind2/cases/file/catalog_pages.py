from django.http import Http404, HttpResponse, HttpResponseBadRequest

PAGES_DIR = "/srv/catalog/rendered"


def catalog_page(request):
    try:
        page = int(request.GET.get("page", "1"))
    except ValueError:
        return HttpResponseBadRequest("page must be a number")
    if page < 1:
        return HttpResponseBadRequest("page must be positive")
    try:
        with open(f"{PAGES_DIR}/page_{page}.html", encoding="utf-8") as fh:
            return HttpResponse(fh.read())
    except FileNotFoundError:
        raise Http404("no such page")
