from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route("/tax/estimate", methods=["POST"])
def tax_estimate():
    rate = float(request.form["rate"])
    base = float(request.form.get("base", 0))
    formula = f"base * (1 + {rate})"
    return jsonify(gross=eval(formula, {"__builtins__": {}}, {"base": base}))
