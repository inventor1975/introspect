from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from lib.models import PricingRule


def apply_rule(request, code):
    rule = get_object_or_404(PricingRule, code=code, active=True)
    variables = {
        "base": float(request.GET.get("base", 0)),
        "qty": int(request.GET.get("qty", 1)),
        "region": request.GET.get("region", "EU"),
    }
    price = eval(rule.expression, {"__builtins__": {}}, variables)
    return JsonResponse({"rule": code, "price": price})
