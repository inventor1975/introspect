from flask import Flask, request
from markupsafe import escape

app = Flask(__name__)


@app.route("/invoice")
def invoice():
    raw = request.args.get("invoice", "")
    try:
        number = int(raw)
    except ValueError:
        return f"<p class='error'>Invoice '{escape(raw)}' was not found.</p>", 404
    return f"<p>Invoice #{number:06d}</p>"
