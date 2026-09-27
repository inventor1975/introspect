import html

from flask import Flask, request

app = Flask(__name__)


@app.route("/alert")
def alert():
    msg = request.args.get("msg", "")
    if request.args.get("urgent") == "1":
        text = "<strong>Urgent:</strong> " + html.escape(msg)
    else:
        text = html.escape(msg)
    return '<div class="alert">' + text + "</div>"
