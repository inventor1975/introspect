import json

from django.http import HttpResponse


def widget_config(request):
    config = {
        "title": request.GET.get("title", "Dashboard"),
        "refresh": 30,
        "compact": request.GET.get("compact") == "1",
    }
    page = (
        "<html><body><div id='app'></div>"
        "<script>window.WIDGET_CONFIG = " + json.dumps(config) + ";</script>"
        "<script src='/static/widget.js'></script></body></html>"
    )
    return HttpResponse(page)
