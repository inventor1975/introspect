from django.http import HttpResponse
from django.utils.html import format_html


def welcome(request):
    name = request.GET.get("name", "guest")
    unread = request.GET.get("unread", "0")
    snippet = format_html(
        "<p>Welcome, <b>{}</b>! You have {} new messages.</p>", name, unread
    )
    return HttpResponse(snippet)
