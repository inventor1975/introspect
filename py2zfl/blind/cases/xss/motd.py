import html

from flask import Flask, request

app = Flask(__name__)


@app.route("/motd/preview", methods=["POST"])
def motd_preview():
    text = request.form.get("text", "")
    text = text.strip()
    text = html.escape(text)
    text = text.replace("\n", "<br>")
    return f"<div class='motd'>{text}</div>"
