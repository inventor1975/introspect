import os

from django.contrib.admin.views.decorators import staff_member_required
from django.db import connection
from django.shortcuts import render

AUDIT_TABLE = os.environ.get("AUDIT_TABLE", "security_auditevent")


@staff_member_required
def audit_log(request):
    actor = request.GET.get("actor", "")
    sql = f"SELECT occurred_at, actor, event, ip FROM {AUDIT_TABLE} WHERE actor = %s ORDER BY occurred_at DESC"
    with connection.cursor() as cursor:
        cursor.execute(sql, [actor])
        events = cursor.fetchall()
    return render(request, "security/audit_log.html", {"events": events, "actor": actor})
