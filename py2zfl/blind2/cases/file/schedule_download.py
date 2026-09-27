from django.http import FileResponse, HttpResponseBadRequest

DAILY = "/srv/transit/schedules/daily.gtfs.zip"
WEEKLY = "/srv/transit/schedules/weekly.gtfs.zip"
HOLIDAY = "/srv/transit/schedules/holiday.gtfs.zip"


def schedule_file(request):
    kind = request.GET.get("kind", "daily")
    if kind == "daily":
        path = DAILY
    elif kind == "weekly":
        path = WEEKLY
    elif kind == "holiday":
        path = HOLIDAY
    else:
        return HttpResponseBadRequest(f"unknown schedule kind: {kind}")
    return FileResponse(open(path, "rb"), as_attachment=True)
