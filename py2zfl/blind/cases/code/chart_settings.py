import ast

from flask import Flask, abort, jsonify, request

app = Flask(__name__)

SCALE_EXPR = "[round(v * factor + offset, precision) for v in values]"


@app.route("/charts/scale", methods=["POST"])
def scale_values():
    try:
        settings = ast.literal_eval(request.get_data(as_text=True))
    except (ValueError, SyntaxError):
        abort(400)
    if not isinstance(settings, dict):
        abort(400)
    scope = {
        "values": settings.get("values", []),
        "factor": settings.get("factor", 1),
        "offset": settings.get("offset", 0),
        "precision": settings.get("precision", 2),
        "round": round,
    }
    return jsonify(scaled=eval(SCALE_EXPR, {"__builtins__": {}}, scope))
