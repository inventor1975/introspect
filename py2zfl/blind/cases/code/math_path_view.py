from django.http import JsonResponse
from django.urls import path
from django.views.decorators.http import require_GET


@require_GET
def evaluate_expression(request, expression):
    precision = int(request.GET.get("precision", 4))
    value = eval(expression)
    if isinstance(value, float):
        value = round(value, precision)
    return JsonResponse({"expression": expression, "value": value})


urlpatterns = [
    path("math/<str:expression>/", evaluate_expression, name="evaluate-expression"),
]
