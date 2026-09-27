from django.http import HttpResponse
from django.template import Context, Template

_RESULTS = Template(
    "{% autoescape off %}<h2>Results for {{ query }}</h2>{% endautoescape %}"
    "<p>{{ count }} matches</p>"
)


def results(request):
    query = request.GET.get("q", "")
    html = _RESULTS.render(Context({"query": query, "count": 0}))
    return HttpResponse(html)
