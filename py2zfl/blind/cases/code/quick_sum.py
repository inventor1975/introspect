import re

from flask import Flask, abort, jsonify, request

app = Flask(__name__)

SIMPLE_ARITHMETIC = re.compile(r"\d{1,6}(?:\s*[-+*/]\s*\d{1,6}){0,8}")


@app.route("/quick-sum")
def quick_sum():
    expr = request.args.get("q", "").strip()
    if not SIMPLE_ARITHMETIC.fullmatch(expr):
        abort(400, "only simple arithmetic is supported")
    try:
        return jsonify(result=eval(expr))
    except ZeroDivisionError:
        abort(400, "division by zero")
