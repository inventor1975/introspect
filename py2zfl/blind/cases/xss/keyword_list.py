from flask import Flask, request
from markupsafe import escape

app = Flask(__name__)


@app.route("/keywords")
def keywords():
    words = request.args.getlist("kw")
    out = "<ul class='keywords'>"
    for w in words:
        out += f"<li>{escape(w.lower())}</li>"
    out += "</ul>"
    return out
