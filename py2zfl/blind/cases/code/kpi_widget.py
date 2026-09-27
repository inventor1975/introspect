import logging

from flask import Flask, jsonify, request

app = Flask(__name__)
log = logging.getLogger(__name__)

DEFAULT_EXPR = "orders / visits * 100 if visits else 0"


@app.route("/kpi/conversion")
def conversion():
    expr = request.args.get("expr", "")
    if expr:
        log.info("custom kpi expression requested: %r", expr)
    expr = DEFAULT_EXPR
    stats = {"orders": 42, "visits": 1830}
    return jsonify(conversion=eval(expr, {}, stats))
