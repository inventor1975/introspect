from django.http import HttpResponse
from django.views import View


class OrderStatusView(View):
    http_method_names = ["get"]

    def get(self, request, *args, **kwargs):
        reference = self.request.GET.get("ref", "")
        note = self.request.GET.get("note", "")
        return HttpResponse(self._render(reference, note))

    def _render(self, reference, note):
        parts = ["<div class='order'>"]
        parts.append(f"<h3>Order {reference}</h3>")
        if note:
            parts.append(f"<p class='note'>{note}</p>")
        parts.append("</div>")
        return "\n".join(parts)
