import html

from flask import Flask, request

app = Flask(__name__)


@app.route("/glossary/entry")
def entry():
    word = request.args.get("word", "")
    hint = request.args.get("hint", "")
    return (
        '<span class="term" title="' + html.escape(hint) + '">'
        + html.escape(word)
        + "</span>"
    )
