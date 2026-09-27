from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST

from lib.models import SavedFormula


@login_required
@require_POST
def save_formula(request):
    formula = SavedFormula.objects.create(
        owner=request.user,
        name=request.POST.get("name", "untitled"),
        expression=request.POST["expression"],
    )
    return JsonResponse({"id": formula.pk}, status=201)


@login_required
def apply_formula(request, formula_id):
    formula = get_object_or_404(SavedFormula, pk=formula_id, owner=request.user)
    x = float(request.GET.get("x", 0))
    return JsonResponse({"value": eval(formula.expression, {"x": x})})
