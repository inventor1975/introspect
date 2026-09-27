from django.http import Http404, JsonResponse

from lib.reports import UnknownReport, run_report


def report(request, name):
    params = {
        "revenue": request.GET.get("revenue", 0),
        "cost": request.GET.get("cost", 0),
        "current": request.GET.get("current", 0),
        "previous": request.GET.get("previous", 0),
        "orders": request.GET.get("orders", 0),
    }
    try:
        value = run_report(name, params)
    except UnknownReport:
        raise Http404(name)
    except ValueError:
        return JsonResponse({"error": "parameters must be numeric"}, status=400)
    return JsonResponse({"report": name, "value": value})
