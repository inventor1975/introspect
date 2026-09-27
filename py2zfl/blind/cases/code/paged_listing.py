from flask import Flask, request, render_template_string

app = Flask(__name__)


def fetch_items(page, per_page):
    start = (page - 1) * per_page
    return [f"item-{i}" for i in range(start, start + per_page)]


@app.route("/items")
def items():
    page = int(request.args.get("page", 1))
    per_page = min(int(request.args.get("per_page", 20)), 100)
    header = f"<h2>Page {page}</h2>"
    body = header + "<ul>{% for i in items %}<li>{{ i }}</li>{% endfor %}</ul>"
    return render_template_string(body, items=fetch_items(page, per_page))
