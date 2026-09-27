from django.http import HttpResponse
from django.utils.html import format_html

ROLES = {"a": "Admin", "e": "Editor", "v": "Viewer"}


def nameplate(request):
    name = request.GET.get("name", "")
    role = ROLES.get(request.GET.get("role", "v"), "Viewer")
    plate = format_html("<span class='nameplate'>{} &middot; {}</span>", name, role)
    return HttpResponse(plate)
