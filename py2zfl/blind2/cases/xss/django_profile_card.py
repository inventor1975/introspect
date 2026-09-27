from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.utils.safestring import mark_safe

from accounts.models import Profile


@login_required
def profile_card(request, username):
    profile = get_object_or_404(Profile, user__username=username)
    about = mark_safe(profile.about_html)
    return HttpResponse(
        f"<div class='profile-card'><h3>{profile.user.get_full_name()}</h3>{about}</div>"
    )
