from datetime import date, timedelta

from django.db import connection
from django.http import HttpResponseBadRequest, JsonResponse


def bookings_between(request):
    try:
        start = date.fromisoformat(request.GET["from"])
        end = date.fromisoformat(request.GET.get("to", "")) if request.GET.get("to") else start + timedelta(days=7)
    except (KeyError, ValueError):
        return HttpResponseBadRequest("from/to must be YYYY-MM-DD")
    sql = (
        "SELECT room_id, guest_name, check_in, check_out FROM bookings_booking "
        f"WHERE check_in >= '{start.isoformat()}' AND check_in < '{end.isoformat()}' "
        "ORDER BY check_in"
    )
    with connection.cursor() as cursor:
        cursor.execute(sql)
        rows = cursor.fetchall()
    return JsonResponse({"bookings": [list(map(str, r)) for r in rows]})
