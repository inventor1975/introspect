from flask import Flask, request

from lib.fragments import render_card

app = Flask(__name__)


@app.route("/widgets/card")
def card():
    title = request.args.get("title", "Untitled")
    body = "Created with the widget builder."
    return render_card(title, body)
