from flask import Flask, request

app = Flask(__name__)


@app.route("/cart/count-label")
def cart_label():
    raw = request.args.get("count", "0")
    try:
        count = int(raw)
        label = f"{count} item" + ("" if count == 1 else "s")
    except ValueError:
        label = raw
    return f"<span class='cart-count'>{label}</span>"
