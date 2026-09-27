from urllib.parse import unquote_plus

from flask import Flask, request
from markupsafe import escape

app = Flask(__name__)


@app.route("/signup")
def signup():
    ref = str(escape(request.args.get("ref", "")))
    ref = unquote_plus(ref)
    note = f"<p class='ref'>Referred by {ref}</p>" if ref else ""
    return "<h1>Create your account</h1>" + note + "<form method='post'></form>"
