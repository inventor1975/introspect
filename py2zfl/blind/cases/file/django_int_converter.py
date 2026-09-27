import os

from django.conf import settings
from django.http import FileResponse, Http404
from django.urls import path

LABEL_DIR = os.path.join(settings.MEDIA_ROOT, "shipping_labels")


def shipping_label(request, order_id):
    label = os.path.join(LABEL_DIR, "order-{}.pdf".format(order_id))
    if not os.path.exists(label):
        raise Http404("label not generated yet")
    return FileResponse(open(label, "rb"), content_type="application/pdf")


urlpatterns = [
    path("orders/<int:order_id>/label/", shipping_label, name="shipping-label"),
]
