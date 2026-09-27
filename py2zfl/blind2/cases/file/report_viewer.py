import os

from django.http import FileResponse, Http404, HttpResponseBadRequest
from django.urls import path
from django.views.decorators.http import require_GET

REPORT_ROOT = "/var/lib/analytics/reports"


@require_GET
def view_report(request):
    report = request.GET.get("report", "").strip()
    if not report:
        return HttpResponseBadRequest("report is required")
    full_path = os.path.join(REPORT_ROOT, report)
    try:
        handle = open(full_path, "rb")
    except FileNotFoundError:
        raise Http404("no such report")
    return FileResponse(handle, filename=os.path.basename(full_path))


urlpatterns = [
    path("reports/view/", view_report, name="view-report"),
]
