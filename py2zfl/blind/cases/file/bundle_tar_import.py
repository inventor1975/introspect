import tarfile

from django.conf import settings
from django.contrib.auth.decorators import permission_required
from django.http import HttpResponseBadRequest, JsonResponse
from django.views.decorators.http import require_POST


@require_POST
@permission_required("content.import_bundle")
def import_bundle(request):
    upload = request.FILES.get("bundle")
    if upload is None:
        return HttpResponseBadRequest("bundle required")
    with tarfile.open(fileobj=upload.file, mode="r:gz") as tar:
        names = tar.getnames()
        tar.extractall(path=settings.CONTENT_IMPORT_DIR)
    return JsonResponse({"imported": names})
