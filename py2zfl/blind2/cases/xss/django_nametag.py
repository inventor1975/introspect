from django.http import HttpResponse
from django.utils.html import format_html

ROLES = {"a": "Admin", "e": "Editor", "v": "Viewer"}


def nametag(request):
    name = request.GET.get("name", "")
    role = ROLES.get(request.GET.get("role", "v"), "Viewer")
    tag = format_html("<span class='nametag'>" + name + " &middot; {}</span>", role)
    return HttpResponse(tag)
