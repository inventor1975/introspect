from flask import Flask, request
from markupsafe import escape

app = Flask(__name__)


@app.route("/listings")
def listings():
    chips = ""
    for key, value in request.args.items(multi=True):
        if key in ("page", "sort"):
            continue
        chips += f"<span class='chip'><b>{escape(key)}</b>: {value}</span>"
    header = "<div class='active-filters'>" + (chips or "No filters") + "</div>"
    return header + "<div id='results'></div>"
