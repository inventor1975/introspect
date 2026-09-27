from datetime import datetime

from django.db import connection
from django.http import HttpResponseBadRequest, JsonResponse


def daily_metrics(request):
    raw_day = request.GET.get("day", "")
    try:
        day = datetime.strptime(raw_day, "%Y-%m-%d").date()
    except ValueError:
        return HttpResponseBadRequest("day must be YYYY-MM-DD")
    stamp = day.isoformat()
    with connection.cursor() as cur:
        cur.execute(
            "SELECT metric, value FROM metrics_daily WHERE day = '" + stamp + "' ORDER BY metric"
        )
        data = dict(cur.fetchall())
    return JsonResponse({"day": stamp, "metrics": data})
