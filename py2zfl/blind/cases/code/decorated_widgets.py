import functools

from flask import Flask, abort, jsonify, request

app = Flask(__name__)


def with_payload(*fields):
    def decorator(view):
        @functools.wraps(view)
        def wrapper(*args, **kwargs):
            body = request.get_json(silent=True) or {}
            for field in fields:
                if field not in body:
                    abort(400, f"missing {field}")
                kwargs[field] = body[field]
            return view(*args, **kwargs)
        return wrapper
    return decorator


@app.route("/widgets/computed", methods=["POST"])
@with_payload("label", "expr")
def computed_widget(label, expr):
    metrics = {"visits": 1200, "signups": 87}
    value = eval(expr, {}, metrics)
    return jsonify(label=label, value=value)
