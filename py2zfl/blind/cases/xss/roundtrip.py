import html

from flask import Flask, request

app = Flask(__name__)


@app.route("/quote")
def quote():
    raw = request.args.get("text", "")
    cleaned = html.escape(raw)
    # users often paste already-encoded text such as &amp;amp; from emails
    normalised = html.unescape(cleaned)
    return "<blockquote>%s</blockquote>" % normalised
