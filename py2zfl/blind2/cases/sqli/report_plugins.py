import importlib

from django.conf import settings
from django.db import connection
from django.http import JsonResponse


def load_backend():
    module = importlib.import_module(settings.REPORT_FILTER_BACKEND)
    return module.FilterBackend()


def report(request):
    backend = load_backend()
    where = backend.where_clause(request.GET.dict())
    with connection.cursor() as cur:
        cur.execute(f"SELECT day, visits, signups FROM analytics_daily WHERE {where} ORDER BY day")
        rows = cur.fetchall()
    return JsonResponse({"rows": [[str(r[0]), r[1], r[2]] for r in rows]})
