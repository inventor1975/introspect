from flask import Flask, request
from markupsafe import Markup

app = Flask(__name__)


@app.route("/address/preview", methods=["POST"])
def address_preview():
    lines = request.form.get("address", "").splitlines()
    return Markup("<address>") + Markup("<br>\n").join(lines) + Markup("</address>")
