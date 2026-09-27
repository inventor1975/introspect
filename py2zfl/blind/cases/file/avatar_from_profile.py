import os

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import FileResponse, JsonResponse
from django.views.decorators.http import require_POST

from .models import Profile

AVATAR_ROOT = os.path.join(settings.MEDIA_ROOT, "avatars")


@login_required
@require_POST
def choose_avatar(request):
    profile = Profile.objects.get(user=request.user)
    profile.avatar_file = request.POST.get("avatar", "default.png")
    profile.save(update_fields=["avatar_file"])
    return JsonResponse({"ok": True})


@login_required
def avatar_image(request):
    profile = Profile.objects.get(user=request.user)
    path = os.path.join(AVATAR_ROOT, profile.avatar_file)
    return FileResponse(open(path, "rb"), content_type="image/png")
