from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .models import Member


@login_required
def member_search(request):
    city = request.GET.get("city")
    members = Member.objects.filter(active=True).order_by("last_name")
    if city:
        members = members.extra(where=["lower(city) = lower(%s)"], params=[city])
    return render(request, "members/directory.html", {"members": members, "city": city})
