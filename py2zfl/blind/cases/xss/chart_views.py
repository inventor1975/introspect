from django.http import HttpResponse
from django.utils.html import format_html, json_script


def chart(request):
    series = {
        "label": request.GET.get("label", "Visits"),
        "points": [3, 7, 4, 9],
    }
    return HttpResponse(
        format_html(
            "<canvas id='c'></canvas>{}<script src='/static/chart.js'></script>",
            json_script(series, "chart-data"),
        )
    )
