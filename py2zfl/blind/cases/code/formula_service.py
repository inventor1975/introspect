import math

from flask import Flask, jsonify, request

app = Flask(__name__)


class FormulaEngine:
    def __init__(self, precision=2):
        self.precision = precision
        self.scope = {"sqrt": math.sqrt, "pi": math.pi}

    def evaluate(self, expression, **variables):
        scope = dict(self.scope, **variables)
        return round(eval(expression, scope), self.precision)


engine = FormulaEngine()


@app.route("/geometry/area", methods=["POST"])
def area():
    data = request.get_json()
    shape_formula = data.get("formula", "pi * r ** 2")
    radius = float(data.get("r", 1))
    return jsonify(area=engine.evaluate(shape_formula, r=radius))
