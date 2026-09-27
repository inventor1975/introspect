import uuid

from django.contrib.auth.decorators import login_required
from django.db import connection
from django.http import HttpResponseBadRequest, JsonResponse
from django.views.decorators.http import require_POST


@login_required
@require_POST
def revoke_device(request):
    try:
        device = uuid.UUID(request.POST.get("device_id", ""))
    except ValueError:
        return HttpResponseBadRequest("invalid device id")
    with connection.cursor() as cur:
        cur.execute(
            f"UPDATE accounts_device SET revoked = TRUE WHERE token = '{device}' "
            f"AND user_id = {int(request.user.pk)}"
        )
        count = cur.rowcount
    return JsonResponse({"revoked": count})
