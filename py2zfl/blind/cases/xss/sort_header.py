from flask import Flask, request

app = Flask(__name__)

ALLOWED_SORT = {"name", "date", "size"}


@app.route("/files")
def files():
    sort = request.args.get("sort", "name")
    folder = request.args.get("folder", "/")
    if sort not in ALLOWED_SORT:
        sort = "name"
    return f"<h2>Contents of {folder}</h2><p>Sorted by {sort}</p>"
