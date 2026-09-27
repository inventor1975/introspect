from django.http import HttpResponse
from django.template import Context, Template

SUMMARY = Template(
    "<p>{{ count }} result{{ count|pluralize }} for <strong>{{ q }}</strong></p>"
)


def search_summary(request):
    q = request.GET.get("q", "")
    count = len(q.split())
    return HttpResponse(SUMMARY.render(Context({"q": q, "count": count})))
