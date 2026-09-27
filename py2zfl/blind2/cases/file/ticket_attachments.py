from django.db import models
from django.http import FileResponse, Http404, JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_GET, require_POST


class Attachment(models.Model):
    ticket_id = models.IntegerField()
    stored_path = models.CharField(max_length=500)
    label = models.CharField(max_length=200, blank=True)


@require_POST
def link_attachment(request, ticket_id):
    attachment = Attachment.objects.create(
        ticket_id=ticket_id,
        stored_path=request.POST["stored_path"],
        label=request.POST.get("label", ""),
    )
    return JsonResponse({"id": attachment.pk}, status=201)


@require_GET
def download_attachment(request, ticket_id, attachment_id):
    attachment = get_object_or_404(Attachment, pk=attachment_id, ticket_id=ticket_id)
    try:
        handle = open(attachment.stored_path, "rb")
    except OSError:
        raise Http404("attachment missing on disk")
    return FileResponse(handle, filename=attachment.label or None)
