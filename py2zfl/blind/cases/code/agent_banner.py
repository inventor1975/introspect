from django.http import HttpResponse
from django.template import Context
from django.template.engine import Engine


def unsupported_browser(request):
    agent = request.META.get("HTTP_USER_AGENT", "unknown")
    source = (
        "<p>Your browser (" + agent + ") is not supported.</p>"
        "<p>Please upgrade to one of: {{ supported|join:', ' }}</p>"
    )
    template = Engine.get_default().from_string(source)
    body = template.render(Context({"supported": ["Firefox", "Chrome", "Safari"]}))
    return HttpResponse(body, status=406)
