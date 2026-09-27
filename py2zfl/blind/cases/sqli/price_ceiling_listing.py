from django.http import JsonResponse
from django.views import View

from catalog.models import Product


class ProductListView(View):
    def get(self, request):
        qs = Product.objects.filter(active=True)
        max_price = request.GET.get("max_price")
        if max_price:
            qs = qs.extra(where=[f"price <= {max_price}"])
        data = list(qs.values("id", "name", "price")[:100])
        return JsonResponse({"products": data})
