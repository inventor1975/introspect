from django.contrib.auth.decorators import login_required
from django.db import connection
from django.http import HttpResponseNotAllowed, JsonResponse


@login_required
def remove_attachments(request):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])
    ticket = request.POST.get("ticket_id", "")
    with connection.cursor() as cursor:
        cursor.execute(
            "DELETE FROM helpdesk_attachment WHERE ticket_id = " + ticket + " AND owner_id = %s",
            [request.user.id],
        )
        removed = cursor.rowcount
    return JsonResponse({"removed": removed})
