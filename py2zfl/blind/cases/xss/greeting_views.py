from django.http import HttpResponse
from django.utils.html import format_html


def greeting(request):
    name = request.GET.get("name", "guest")
    city = request.GET.get("city", "somewhere")
    snippet = format_html(f"<p>Hi <b>{name}</b>, last seen in {{}}</p>", city)
    return HttpResponse(snippet)
