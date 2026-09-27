from flask import Blueprint, abort, jsonify, request

bp = Blueprint("rules", __name__, url_prefix="/rules")


def _load_rows():
    return [
        {"sku": "A-1", "price": 12.5, "stock": 4},
        {"sku": "B-7", "price": 3.0, "stock": 0},
    ]


@bp.route("/check", methods=["POST"])
def check_rules():
    payload = request.get_json(silent=True) or {}
    rules = payload.get("rules")
    if not isinstance(rules, list):
        abort(400)
    results = []
    for rule in rules:
        compiled = compile(rule["cond"], "<rule:%s>" % rule.get("id", "?"), "eval")
        matches = [row["sku"] for row in _load_rows() if eval(compiled, {}, row)]
        results.append({"id": rule.get("id"), "matches": matches})
    return jsonify(results)
