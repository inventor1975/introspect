from html import escape

from flask import Flask, request

app = Flask(__name__)


@app.route("/subscribe")
def subscribe_form():
    email = request.args.get("email", "")
    source = request.args.get("utm_source", "direct")
    return (
        "<form method='post' action='/subscribe'>"
        f'<input type="email" name="email" value="{escape(email)}">'
        f'<input type="hidden" name="source" value="{escape(source)}">'
        "<button>Subscribe</button></form>"
    )
