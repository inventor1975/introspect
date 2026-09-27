import json
import os

from django.contrib.admin.views.decorators import staff_member_required
from django.http import Http404, JsonResponse

BACKUP_ROOT = os.path.realpath("/var/backups/app")


@staff_member_required
def backup_manifest(request):
    manifest = request.GET.get("manifest", "latest/manifest.json")
    manifest_path = os.path.realpath(os.path.join(BACKUP_ROOT, manifest))
    if not manifest_path.startswith(BACKUP_ROOT + os.sep):
        raise Http404("unknown manifest")
    with open(manifest_path) as fh:
        entries = json.load(fh)
    return JsonResponse({"manifest": manifest, "files": entries.get("files", [])})
