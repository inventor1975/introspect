from django.http import HttpResponse
from django.template.loader import render_to_string
from django.utils.safestring import SafeString


def product_teaser(request):
    tagline = request.GET.get("tagline", "")
    context = {"tagline": SafeString(tagline), "cta": "Buy now"}
    return HttpResponse(render_to_string("shop/teaser.html", context))
