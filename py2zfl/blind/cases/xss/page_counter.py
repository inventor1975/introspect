from flask import Flask, request

app = Flask(__name__)


@app.route("/listing")
def listing():
    page = int(request.args.get("page", "1"))
    per_page = int(request.args.get("per_page", "25"))
    first = (page - 1) * per_page + 1
    return f"<p>Page {page}: items {first} to {first + per_page - 1}</p>"
