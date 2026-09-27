from flask import Flask, request

app = Flask(__name__)

PAGE_SIZE = 20


@app.route("/archive")
def archive():
    raw_page = request.args.get("page", "1")
    try:
        page = int(raw_page)
    except ValueError:
        return f"<p class='error'>'{raw_page}' is not a valid page number.</p>", 400
    start = (page - 1) * PAGE_SIZE
    return f"<p>Showing entries {start + 1} to {start + PAGE_SIZE}</p>"
