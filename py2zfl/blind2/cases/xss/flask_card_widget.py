from flask import Flask, request

from lib.htmlkit import card, page

app = Flask(__name__)


@app.route("/widgets/card")
def card_widget():
    title = request.args.get("title", "Untitled")
    text = request.args.get("text", "")
    return page("Card", card(title, text, css="card card-compact"))
