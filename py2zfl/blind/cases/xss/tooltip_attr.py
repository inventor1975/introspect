import html

from flask import Flask, request

app = Flask(__name__)


@app.route("/glossary/term")
def term():
    word = request.args.get("word", "")
    hint = request.args.get("hint", "")
    safe_word = html.escape(word)
    hint_attr = html.escape(hint, quote=False)
    return '<span class="term" title="' + hint_attr + '">' + safe_word + "</span>"
