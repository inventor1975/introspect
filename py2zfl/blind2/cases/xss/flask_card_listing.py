from flask import Flask, request

from lib.htmlkit import card_escaped, page

app = Flask(__name__)


@app.route("/widgets/note")
def note_widget():
    title = request.args.get("title", "Note")
    text = request.args.get("text", "")
    return page(title, card_escaped(title, text, css="card card-note"))
