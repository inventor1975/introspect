from flask import Flask, request

app = Flask(__name__)

ENTRIES = [f"Entry {i}" for i in range(1, 201)]
PER_PAGE = 20


@app.route("/entries")
def entries():
    try:
        page = int(request.args.get("page", "1"))
    except ValueError:
        return "<p class='error'>The page parameter must be a whole number.</p>", 400
    page = max(page, 1)
    start = (page - 1) * PER_PAGE
    rows = "".join(f"<li>{e}</li>" for e in ENTRIES[start:start + PER_PAGE])
    return f"<h3>Page {page}</h3><ol start='{start + 1}'>{rows}</ol>"
