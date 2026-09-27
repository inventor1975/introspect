import sqlite3

from flask import Flask, abort, render_template, request

app = Flask(__name__)
PER_PAGE = 24


@app.route("/gallery")
def gallery():
    try:
        page = int(request.args.get("page", "1"))
    except ValueError:
        abort(400)
    page = max(page, 1)
    offset = (page - 1) * PER_PAGE
    conn = sqlite3.connect("gallery.db")
    photos = conn.execute(
        "SELECT id, title, thumb_url FROM photos WHERE published = 1 ORDER BY taken_at DESC "
        "LIMIT %d OFFSET %d" % (PER_PAGE, offset)
    ).fetchall()
    conn.close()
    return render_template("gallery.html", photos=photos, page=page)
