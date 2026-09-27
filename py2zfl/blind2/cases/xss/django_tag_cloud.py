from django.http import HttpResponse
from django.template import Context, Template
from django.utils.safestring import mark_safe

CLOUD = Template("<div class='cloud'>{{ tags }}</div>")


def tag_cloud(request):
    tags = request.GET.getlist("tag")
    pills = mark_safe("".join(f"<span class='pill'>{t}</span>" for t in tags))
    return HttpResponse(CLOUD.render(Context({"tags": pills})))
