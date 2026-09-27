from flask import Flask, jsonify, request
from sympy import Symbol, solve, sympify

app = Flask(__name__)


@app.route("/solve")
def solve_equation():
    equation = request.args.get("eq", "x**2 - 4")
    x = Symbol("x")
    expr = sympify(equation)
    return jsonify(roots=[str(r) for r in solve(expr, x)])
