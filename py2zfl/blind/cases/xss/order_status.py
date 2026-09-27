import re

from flask import Flask, abort, request

app = Flask(__name__)

ORDER_REF = re.compile(r"[A-Z]{2}-\d{6}")


@app.route("/orders/status")
def order_status():
    ref = request.args.get("ref", "")
    if not ORDER_REF.fullmatch(ref):
        abort(400)
    return f"<p>Order <b>{ref}</b> is being prepared.</p>"
