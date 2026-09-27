from django.http import JsonResponse


def shipping_estimate(request):
    raw_weight = request.GET.get("weight", "")
    try:
        weight = int(raw_weight)
    except ValueError:
        weight = 0
    zone = 3
    cost = eval(f"{weight} * 0.45 + zone * 1.5", {"zone": zone})
    return JsonResponse({"weight": weight, "cost": round(cost, 2)})
