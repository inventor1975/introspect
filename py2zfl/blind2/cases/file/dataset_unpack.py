import os
import zipfile

from django.http import HttpResponseBadRequest, JsonResponse
from django.views.decorators.http import require_POST

DATASETS = "/srv/ml/datasets"


@require_POST
def unpack_dataset(request):
    upload = request.FILES.get("dataset")
    if upload is None:
        return HttpResponseBadRequest("dataset missing")
    destination = os.path.join(DATASETS, "staging")
    os.makedirs(destination, exist_ok=True)
    written = []
    with zipfile.ZipFile(upload) as archive:
        for info in archive.infolist():
            if info.is_dir():
                continue
            out_path = os.path.join(destination, info.filename)
            os.makedirs(os.path.dirname(out_path), exist_ok=True)
            with open(out_path, "wb") as out:
                out.write(archive.read(info))
            written.append(info.filename)
    return JsonResponse({"files": written})
