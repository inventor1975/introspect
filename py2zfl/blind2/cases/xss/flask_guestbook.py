import sqlite3

from flask import Flask, g, redirect, render_template_string, request, url_for

app = Flask(__name__)
DATABASE = "guestbook.db"

BOOK = """
<h1>Guestbook</h1>
<form method="post"><textarea name="entry"></textarea><button>Sign</button></form>
{% for who, entry in entries %}
  <article><h5>{{ who }}</h5><div>{{ entry|safe }}</div></article>
{% endfor %}
"""


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DATABASE)
    return g.db


@app.route("/guestbook", methods=["GET", "POST"])
def guestbook():
    db = get_db()
    if request.method == "POST":
        db.execute(
            "INSERT INTO entries (who, entry) VALUES (?, ?)",
            (request.form.get("who", "anon"), request.form["entry"]),
        )
        db.commit()
        return redirect(url_for("guestbook"))
    entries = db.execute("SELECT who, entry FROM entries ORDER BY id DESC LIMIT 50").fetchall()
    return render_template_string(BOOK, entries=entries)
