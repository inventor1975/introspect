from django.db import connection
from django.http import JsonResponse

from dbkit.literals import quote_literal


def quoted_search(request):
    term = request.GET.get("q", "")
    literal = quote_literal("%" + term + "%")
    with connection.cursor() as cur:
        cur.execute(
            "SELECT id, name FROM crm_company WHERE name ILIKE " + literal + " ORDER BY name LIMIT 50"
        )
        rows = cur.fetchall()
    return JsonResponse({"companies": [{"id": r[0], "name": r[1]} for r in rows]})
