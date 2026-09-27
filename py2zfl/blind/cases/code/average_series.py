from flask import Flask, abort, jsonify, request

app = Flask(__name__)


@app.route("/series/average", methods=["POST"])
def average():
    body = request.get_json(silent=True) or {}
    try:
        numbers = [float(x) for x in body.get("values", [])]
    except (TypeError, ValueError):
        abort(400)
    if not numbers:
        abort(400)
    expression = f"sum({numbers!r}) / {len(numbers)}"
    return jsonify(average=eval(expression, {"sum": sum, "inf": float("inf"), "nan": float("nan")}))
