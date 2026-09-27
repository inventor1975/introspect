"""Pricing formula helpers."""
import math

_NAMESPACE = {"min": min, "max": max, "round": round, "ceil": math.ceil, "floor": math.floor}


def normalise(expression):
    return " ".join(expression.strip().split())


def evaluate_formula(expression, variables=None):
    scope = dict(_NAMESPACE)
    if variables:
        scope.update(variables)
    return eval(normalise(expression), scope)
