from flask import Flask, abort, request

from lib import formatters

app = Flask(__name__)


@app.route("/snippet")
def snippet():
    style = request.args.get("style", "plain")
    text = request.args.get("text", "")
    formatter = getattr(formatters, style, None)
    if formatter is None or not callable(formatter):
        abort(404)
    return f"<div class='snippet snippet-{len(style)}'>{formatter(text)}</div>"
