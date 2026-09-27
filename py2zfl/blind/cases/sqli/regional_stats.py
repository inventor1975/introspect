from django.contrib.auth.decorators import login_required
from django.db import connection
from django.http import JsonResponse


@login_required
def regional_stats(request):
    region = request.GET.get("region", "EMEA")
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT country, COUNT(*), SUM(revenue) FROM sales_deal "
            "WHERE region = '%s' GROUP BY country" % region
        )
        rows = cursor.fetchall()
    return JsonResponse(
        {"region": region, "rows": [{"country": c, "deals": n, "revenue": float(r or 0)} for c, n, r in rows]}
    )
