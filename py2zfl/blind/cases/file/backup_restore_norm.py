import json
import os

from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse

BACKUP_ROOT = "/var/backups/app"


@staff_member_required
def backup_manifest(request):
    manifest = request.GET.get("manifest", "latest/manifest.json")
    manifest_path = os.path.normpath(os.path.join(BACKUP_ROOT, manifest))
    with open(manifest_path) as fh:
        entries = json.load(fh)
    return JsonResponse({"manifest": manifest, "files": entries.get("files", [])})
