from django.http import HttpResponse
from django.views.decorators.http import require_GET


def _profile_header(display_name, city):
    return "<header><h2>{}</h2><small>{}</small></header>".format(display_name, city)


@require_GET
def profile_preview(request):
    display_name = request.GET.get("display_name", "")
    city = request.GET.get("city", "unknown")
    body = _profile_header(display_name.title(), city)
    return HttpResponse("<html><body>" + body + "</body></html>")
