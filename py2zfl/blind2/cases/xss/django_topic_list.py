from django.http import HttpResponse
from django.utils.html import escape
from django.utils.safestring import mark_safe


def topic_list(request):
    topics = request.GET.getlist("topic")
    items = []
    for t in topics:
        items.append("<li class='topic'>%s</li>" % escape(t.strip()))
    listing = mark_safe("<ul>" + "".join(items) + "</ul>")
    return HttpResponse(listing)
