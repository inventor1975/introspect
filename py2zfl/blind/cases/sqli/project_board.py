import sqlite3

from flask import Flask, render_template, request
from flask_login import current_user, login_required

app = Flask(__name__)


@app.route("/board")
@login_required
def project_board():
    if request.args.get("scope") == "mine":
        where = "assignee_id = %d" % current_user.id
    else:
        where = "team = '%s'" % request.args.get("team", "core")
    conn = sqlite3.connect("tracker.db")
    cards = conn.execute(
        "SELECT id, title, column_name FROM cards WHERE " + where + " ORDER BY position"
    ).fetchall()
    conn.close()
    return render_template("board.html", cards=cards)
