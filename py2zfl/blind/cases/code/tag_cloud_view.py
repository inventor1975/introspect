from django.http import HttpResponse
from django.template import Context, Engine
from django.views.generic import View

CLOUD_SOURCE = (
    "<ul class='tags'>{% for tag in tags %}"
    "<li data-weight='{{ forloop.counter }}'>{{ tag }}</li>{% endfor %}</ul>"
    "{% if heading %}<h3>{{ heading }}</h3>{% endif %}"
)


class TagCloudView(View):
    engine = Engine.get_default()

    def get(self, request, *args, **kwargs):
        template = self.engine.from_string(CLOUD_SOURCE)
        context = Context({
            "tags": request.GET.getlist("tag"),
            "heading": request.GET.get("heading", ""),
        })
        return HttpResponse(template.render(context))
