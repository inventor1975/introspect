import sqlite3

from flask import Flask, g, redirect, render_template_string, request, url_for

app = Flask(__name__)
DATABASE = "board.db"

BOARD = """
<h1>Message board</h1>
<form method="post"><input name="title"><textarea name="text"></textarea><button>Post</button></form>
{% for title, text in posts %}
  <article><h5>{{ title }}</h5><p>{{ text }}</p></article>
{% endfor %}
"""


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DATABASE)
    return g.db


@app.route("/board", methods=["GET", "POST"])
def board():
    db = get_db()
    if request.method == "POST":
        db.execute(
            "INSERT INTO posts (title, text) VALUES (?, ?)",
            (request.form.get("title", ""), request.form.get("text", "")),
        )
        db.commit()
        return redirect(url_for("board"))
    posts = db.execute("SELECT title, text FROM posts ORDER BY id DESC LIMIT 50").fetchall()
    return render_template_string(BOARD, posts=posts)
