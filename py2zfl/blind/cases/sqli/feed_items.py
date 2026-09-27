import sqlite3

from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route("/feed")
def feed_items():
    limit = request.args.get("limit", "20")
    try:
        int(limit)
    except ValueError:
        limit = "20"
    conn = sqlite3.connect("feed.db")
    items = conn.execute(
        "SELECT id, title, url, posted_at FROM items ORDER BY posted_at DESC LIMIT " + limit
    ).fetchall()
    conn.close()
    return jsonify(items)
