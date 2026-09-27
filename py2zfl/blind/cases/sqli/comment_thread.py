import html
import sqlite3

from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/comments")
def comment_thread():
    post_id = html.escape(request.args.get("post", "0"))
    conn = sqlite3.connect("blog.db")
    cur = conn.cursor()
    cur.execute(
        "SELECT author, body, created_at FROM comments "
        f"WHERE post_id = {post_id} AND approved = 1 ORDER BY created_at"
    )
    comments = cur.fetchall()
    conn.close()
    return render_template("comments.html", comments=comments, post_id=post_id)
