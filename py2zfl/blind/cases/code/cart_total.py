from flask import Flask, jsonify, request

app = Flask(__name__)

TOTAL_FORMULA = "price * qty * (1 - discount) + shipping"


@app.route("/cart/total", methods=["POST"])
def cart_total():
    data = request.get_json(force=True)
    variables = {
        "price": data.get("price", 0),
        "qty": data.get("qty", 1),
        "discount": data.get("discount", 0),
        "shipping": data.get("shipping", 4.99),
    }
    total = eval(TOTAL_FORMULA, {"__builtins__": {}}, variables)
    return jsonify(total=total)
