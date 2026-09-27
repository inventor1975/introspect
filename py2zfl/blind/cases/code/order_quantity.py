from django.http import HttpResponseBadRequest, JsonResponse

UNIT_PRICE = 12.75


def quote(request):
    qty = request.GET.get("qty", "1")
    if not qty.isdigit():
        return HttpResponseBadRequest("qty must be a whole number")
    total = eval(f"{qty} * unit_price", {"unit_price": UNIT_PRICE})
    return JsonResponse({"qty": int(qty), "total": total})
