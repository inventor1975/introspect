from flask import Flask, request

app = Flask(__name__)

PRODUCTS = [
    "Walnut desk", "Oak shelf", "Birch stool", "Pine bench", "Maple table",
]


@app.route("/search")
def search():
    q = request.args.get("q", "").strip()
    hits = [p for p in PRODUCTS if q.lower() in p.lower()]
    items = "".join(f"<li>{h}</li>" for h in hits)
    if not hits:
        items = "<li class='empty'>Nothing found</li>"
    return f"<h2>Results for {q}</h2><ul class='results'>{items}</ul>"
