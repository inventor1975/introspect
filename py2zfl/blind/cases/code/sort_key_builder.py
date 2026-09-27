from flask import Flask, jsonify, request

app = Flask(__name__)

PRODUCTS = [
    {"name": "lamp", "price": 30, "rating": 4.1},
    {"name": "desk", "price": 220, "rating": 4.7},
    {"name": "chair", "price": 95, "rating": 3.9},
]


@app.route("/products")
def list_products():
    key_expr = request.args.get("sort_by", "p['name']")
    key_fn = eval("lambda p: " + key_expr)
    reverse = request.args.get("desc") == "1"
    return jsonify(sorted(PRODUCTS, key=key_fn, reverse=reverse))
