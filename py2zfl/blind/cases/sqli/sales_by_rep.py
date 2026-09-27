from django.contrib.auth.decorators import login_required
from django.db import connection
from django.http import JsonResponse

COLUMNS = ", ".join(["rep_id", "rep_name", "SUM(amount)", "COUNT(*)"])


@login_required
def sales_by_rep(request):
    region = request.GET.get("region", "EMEA")
    quarter = request.GET.get("quarter", "2026Q3")
    sql = (
        f"SELECT {COLUMNS} FROM sales_deal WHERE region = %s AND quarter = %s "
        "GROUP BY rep_id, rep_name ORDER BY 3 DESC"
    )
    with connection.cursor() as cursor:
        cursor.execute(sql, [region, quarter])
        rows = cursor.fetchall()
    return JsonResponse({"rows": rows})
