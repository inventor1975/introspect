import uuid

from django.contrib.auth.decorators import login_required
from django.db import models
from django.http import FileResponse
from django.shortcuts import get_object_or_404


def _stored_name(instance, filename):
    return f"documents/{instance.owner_id}/{uuid.uuid4().hex}.bin"


class SharedDocument(models.Model):
    owner = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    file = models.FileField(upload_to=_stored_name)


@login_required
def download_document(request, pk):
    doc = get_object_or_404(SharedDocument, pk=pk, owner=request.user)
    return FileResponse(doc.file.open("rb"), as_attachment=True, filename=f"{doc.title}.bin")
