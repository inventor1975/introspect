from django.http import HttpResponse
from django.utils.html import escape
from django.views.decorators.http import require_GET


def _row(label, value):
    return "<tr><th>%s</th><td>%s</td></tr>" % (escape(label), escape(value))


@require_GET
def account_summary(request):
    rows = [
        _row("Name", request.GET.get("name", "")),
        _row("Email", request.GET.get("email", "")),
        _row("Company", request.GET.get("company", "")),
    ]
    return HttpResponse("<table class='summary'>" + "".join(rows) + "</table>")
