from flask import Flask, request
from markupsafe import escape

app = Flask(__name__)

CATALOG = ["Linen shirt", "Wool scarf", "Denim jacket", "Canvas tote"]


@app.route("/catalog/search")
def catalog_search():
    q = request.args.get("q", "").strip()
    matches = [c for c in CATALOG if q.lower() in c.lower()]
    items = "".join(f"<li>{m}</li>" for m in matches) or "<li>No matches</li>"
    return f"<h2>Results for {escape(q)}</h2><ul>{items}</ul>"
