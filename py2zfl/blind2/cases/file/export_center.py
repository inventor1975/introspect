from django.http import FileResponse, Http404
from django.views import View

from lib.exporter import ExportLocator


class ExportDownloadView(View):
    locator = ExportLocator("/srv/erp/exports")

    def get(self, request):
        requested = request.GET.get("file")
        if not requested:
            raise Http404("file parameter missing")
        location = self.locator.locate(requested)
        try:
            return FileResponse(open(location, "rb"), as_attachment=True)
        except OSError:
            raise Http404("export not available")
