import os

from django.conf import settings
from django.http import FileResponse, Http404
from django.views import View


class AttachmentDownloadView(View):
    base_dir = os.path.join(settings.MEDIA_ROOT, "mail_attachments")

    def get(self, request):
        requested = request.GET.get("name", "")
        display_name = os.path.basename(requested)
        path = os.path.join(self.base_dir, requested)
        if not os.path.isfile(path):
            raise Http404
        return FileResponse(open(path, "rb"), as_attachment=True, filename=display_name)
