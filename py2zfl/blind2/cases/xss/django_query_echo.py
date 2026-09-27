from django.http import HttpResponse
from django.template import engines

django_engine = engines["django"]

TEMPLATE = django_engine.from_string(
    "{% autoescape off %}<p>You searched for: {{ q }}</p>{% endautoescape %}"
)


def query_echo(request):
    q = request.GET.get("q", "")
    return HttpResponse(TEMPLATE.render({"q": q}, request))
