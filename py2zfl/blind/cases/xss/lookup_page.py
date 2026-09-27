import html

from flask import Flask, make_response, request

app = Flask(__name__)

PAGE = """<!doctype html>
<title>Lookup</title>
<p>No entries matched <strong>%s</strong>.</p>"""


@app.route("/lookup")
def lookup():
    term = request.args.get("q", "").strip()
    resp = make_response(PAGE % html.escape(term))
    resp.headers["Cache-Control"] = "no-store"
    return resp
