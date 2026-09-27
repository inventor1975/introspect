from django.contrib.admin.views.decorators import staff_member_required
from django.http import Http404, JsonResponse

SNIPPETS = {
    "clear_sessions": "from django.contrib.sessions.models import Session\nresult = Session.objects.all().delete()[0]",
    "count_users": "from django.contrib.auth.models import User\nresult = User.objects.count()",
    "ping": "result = 'pong'",
}


@staff_member_required
def run_maintenance(request):
    name = request.GET.get("task", "")
    source = SNIPPETS.get(name)
    if source is None:
        raise Http404("unknown task")
    namespace = {}
    exec(source, namespace)
    return JsonResponse({"task": name, "result": namespace.get("result")})
