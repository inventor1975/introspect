from django.contrib.auth.decorators import login_required
from django.http import FileResponse
from django.shortcuts import get_object_or_404

from .models import Document


@login_required
def document_download(request, pk):
    document = get_object_or_404(Document, pk=pk, owner=request.user)
    return FileResponse(open(document.storage_path, "rb"), as_attachment=True, filename=document.title)
