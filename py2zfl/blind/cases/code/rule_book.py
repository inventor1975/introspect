from flask import Flask, abort, jsonify, request

app = Flask(__name__)


class RuleBook:
    RULES = {
        "free_shipping": "subtotal >= 50",
        "bulk_discount": "qty >= 10",
        "vip": "tier == 'gold'",
    }

    def __init__(self, context):
        self.context = context

    def eval(self, key):
        source = self.RULES.get(key)
        if source is None:
            raise KeyError(key)
        return eval(source, {"__builtins__": {}}, self.context)


@app.route("/checkout/rule")
def check_rule():
    book = RuleBook({"subtotal": 64.0, "qty": 3, "tier": "silver"})
    try:
        return jsonify(applies=book.eval(request.args.get("rule", "")))
    except KeyError:
        abort(404)
