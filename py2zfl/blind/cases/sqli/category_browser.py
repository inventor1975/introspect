import sqlite3

from flask import Flask, abort, render_template, request

app = Flask(__name__)
CATEGORIES = {"books", "music", "games", "all"}


@app.route("/browse")
def browse():
    category = request.args.get("category", "all")
    sub = request.args.get("sub", "")
    if category not in CATEGORIES:
        abort(400)
    sql = "SELECT id, title, price FROM items WHERE 1 = 1"
    if category != "all":
        sql += f" AND category = '{category}'"
    if sub:
        sql += f" AND subcategory = '{sub}'"
    conn = sqlite3.connect("store.db")
    items = conn.execute(sql + " ORDER BY title").fetchall()
    return render_template("browse.html", items=items)
