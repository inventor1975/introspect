from django.http import JsonResponse
from django.views import View

from catalog.models import Product


class PriceBandView(View):
    def get(self, request):
        qs = Product.objects.filter(active=True)
        max_price = request.GET.get("max_price")
        min_price = request.GET.get("min_price")
        if max_price:
            qs = qs.extra(where=["price <= %s"], params=[max_price])
        if min_price:
            qs = qs.extra(where=["price >= %s"], params=[min_price])
        return JsonResponse({"products": list(qs.values("id", "name", "price")[:100])})
