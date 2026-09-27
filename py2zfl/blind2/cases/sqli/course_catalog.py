from django.db import connection
from django.http import JsonResponse


def course_search(request):
    sql = "SELECT id, code, title FROM academics_course WHERE active = 1"
    params = []
    term = request.GET.get("q", "").strip()
    dept = request.GET.get("dept")
    if dept:
        sql += " AND department_id = %s"
        params.append(dept)
    if term:
        sql += " AND title LIKE '%%" + term + "%%'"
    sql += " ORDER BY code"
    with connection.cursor() as cursor:
        cursor.execute(sql, params)
        courses = [{"id": r[0], "code": r[1], "title": r[2]} for r in cursor.fetchall()]
    return JsonResponse({"courses": courses})
