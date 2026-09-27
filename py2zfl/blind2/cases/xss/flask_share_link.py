from urllib.parse import quote

from flask import Flask, request

app = Flask(__name__)


@app.route("/share")
def share():
    term = request.args.get("term", "")
    encoded = quote(term, safe="")
    return (
        "<p>Share this search:</p>"
        f"<a class='share' href='/search?q={encoded}'>/search?q={encoded}</a>"
    )
