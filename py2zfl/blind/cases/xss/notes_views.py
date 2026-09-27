from django.http import HttpResponse
from django.template import Context, Template

_NOTE = Template(
    "{% autoescape off %}"
    "<div class='note'><h3>{{ title|force_escape }}</h3><p>{{ body|escape }}</p></div>"
    "{% endautoescape %}"
)


def note_preview(request):
    ctx = Context({
        "title": request.POST.get("title", ""),
        "body": request.POST.get("body", ""),
    })
    return HttpResponse(_NOTE.render(ctx))
