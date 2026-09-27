from flask import Flask, request

app = Flask(__name__)


@app.route("/tags")
def tags():
    selected = request.args.getlist("tag")
    out = "<ul class='tags'>"
    for t in selected:
        out += "<li>#" + t.lower() + "</li>"
    out += "</ul>"
    return out
