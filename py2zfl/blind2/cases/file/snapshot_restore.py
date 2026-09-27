import os
import shutil

from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponseBadRequest, JsonResponse
from django.views.decorators.http import require_POST

SNAPSHOT_DIR = "/var/backups/site/snapshots"
LIVE_CONTENT = "/var/www/site/content.json"


@staff_member_required
@require_POST
def restore_snapshot(request):
    snapshot = request.POST.get("snapshot")
    if snapshot is None:
        return HttpResponseBadRequest("snapshot missing")
    source = os.path.join(SNAPSHOT_DIR, snapshot)
    shutil.copyfile(source, LIVE_CONTENT)
    return JsonResponse({"restored": snapshot})
