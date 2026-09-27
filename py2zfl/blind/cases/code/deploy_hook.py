from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST


@staff_member_required
@require_POST
def post_deploy(request):
    release = request.POST.get("release", "unknown")
    scope = {"release": release, "result": None}
    exec(settings.POST_DEPLOY_SNIPPET, scope)
    return JsonResponse({"release": release, "result": scope["result"]})
