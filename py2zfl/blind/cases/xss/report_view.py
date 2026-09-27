from django.http import HttpResponse
from django.views import View


class ReportTitleView(View):
    template = (
        "<html><head><title>{title}</title></head>"
        "<body><h1>{title}</h1><table>{rows}</table></body></html>"
    )

    def get(self, request):
        title = request.GET.get("title", "Monthly report")
        rows = self._rows(request.GET.getlist("metric"))
        return HttpResponse(self._page(title, rows))

    def _page(self, title, rows):
        return self.template.format(title=title, rows=rows)

    def _rows(self, metrics):
        return "".join("<tr><td>%d</td></tr>" % i for i, _ in enumerate(metrics))
