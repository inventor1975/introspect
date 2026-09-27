from flask import Flask, request
from markupsafe import Markup

app = Flask(__name__)


@app.route("/thanks")
def thanks():
    name = request.args.get("name", "customer")
    order = request.args.get("order", "")
    msg = Markup("<p>Thank you, ") + name + Markup("!</p>")
    if order:
        msg += Markup("<p>Your order reference: <code>%s</code></p>") % order
    return msg
