from urllib.parse import unquote

from flask import Flask, request

app = Flask(__name__)


@app.route("/leaving")
def leaving():
    target = unquote(request.args.get("to", "/"))
    return (
        "<p>You are leaving our site.</p>"
        f"<p>Continue to <a href='{target}'>{target}</a>?</p>"
    )
