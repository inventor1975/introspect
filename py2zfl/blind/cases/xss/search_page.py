from flask import Flask, make_response, request

app = Flask(__name__)

PAGE = """<!doctype html>
<title>Search</title>
<p>You searched for: <strong>%s</strong></p>
<p>No results.</p>"""


@app.route("/search")
def search():
    term = request.args.get("q", "").strip()
    resp = make_response(PAGE % term)
    resp.headers["Cache-Control"] = "no-store"
    return resp
