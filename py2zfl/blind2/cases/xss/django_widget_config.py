from django.http import HttpResponse
from django.utils.html import json_script


def widget_bootstrap(request):
    config = {
        "greeting": request.GET.get("greeting", "Hi"),
        "accent": request.GET.get("accent", "#336699"),
    }
    script_tag = json_script(config, "widget-config")
    return HttpResponse(
        "<div id='widget'></div>" + script_tag + "<script src='/static/widget.js'></script>"
    )
