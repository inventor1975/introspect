from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.template import Context, Template

from billing.models import Invoice


def invoice_note(request, invoice_id):
    invoice = get_object_or_404(Invoice, pk=invoice_id)
    note = request.GET.get("note", "Thank you for your business.")
    rendered = Template(note).render(Context({"invoice": invoice}))
    return HttpResponse(rendered)
