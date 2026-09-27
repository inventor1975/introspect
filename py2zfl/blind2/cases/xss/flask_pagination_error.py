from flask import Flask, request

app = Flask(__name__)

POSTS = [f"Post #{i}" for i in range(1, 101)]
PER_PAGE = 10


@app.route("/archive")
def archive():
    try:
        page = int(request.args.get("page", "1"))
    except ValueError as exc:
        return f"<p class='error'>Bad page parameter: {exc}</p>", 400
    start = (page - 1) * PER_PAGE
    rows = "".join(f"<li>{p}</li>" for p in POSTS[start:start + PER_PAGE])
    return f"<ol start='{start + 1}'>{rows}</ol>"
