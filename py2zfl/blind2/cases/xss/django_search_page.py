from django.http import HttpResponse
from django.template import Context, Template

RESULTS = Template(
    "<h2>Results for {{ q }}</h2>"
    "<p>{{ count }} match{{ count|pluralize:'es' }}</p>"
)


def search_page(request):
    q = request.GET.get("q", "")
    count = 0 if not q else len(q.split())
    return HttpResponse(RESULTS.render(Context({"q": q, "count": count})))
