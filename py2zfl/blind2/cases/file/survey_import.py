import os
import zipfile

from django.http import HttpResponseBadRequest, JsonResponse
from django.views.decorators.http import require_POST

IMPORT_ROOT = os.path.realpath("/srv/surveys/imports")


@require_POST
def import_responses(request):
    upload = request.FILES.get("bundle")
    if upload is None:
        return HttpResponseBadRequest("bundle missing")
    extracted = []
    with zipfile.ZipFile(upload) as bundle:
        for member in bundle.infolist():
            if member.is_dir():
                continue
            destination = os.path.realpath(os.path.join(IMPORT_ROOT, member.filename))
            if not destination.startswith(IMPORT_ROOT + os.sep):
                return HttpResponseBadRequest(f"rejected entry {member.filename!r}")
            os.makedirs(os.path.dirname(destination), exist_ok=True)
            with open(destination, "wb") as out:
                out.write(bundle.read(member))
            extracted.append(member.filename)
    return JsonResponse({"imported": extracted})
