import html

from flask import Flask, request

app = Flask(__name__)

KNOWN = {"draft", "review", "published"}


@app.route("/docs/status")
def doc_status():
    status = request.args.get("status", "draft")
    if status in KNOWN:
        label = status.capitalize()
    else:
        label = "Unrecognised status: " + html.escape(status)
    return f"<span class='status'>{label}</span>"
