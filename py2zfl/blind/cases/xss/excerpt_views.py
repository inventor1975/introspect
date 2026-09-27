from django.http import HttpResponse
from django.utils.html import escape
from django.utils.safestring import mark_safe


def excerpt(request):
    text = request.GET.get("text", "")
    snippet = mark_safe("<p class='excerpt'>" + escape(text[:200]) + "&hellip;</p>")
    return HttpResponse(snippet)
