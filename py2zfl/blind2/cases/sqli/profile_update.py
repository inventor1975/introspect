from flask import Flask, redirect, request, session, url_for

from lib.db import get_db

app = Flask(__name__)
app.secret_key = "change-me"

EDITABLE = ["display_name", "bio", "location"]


@app.route("/profile", methods=["POST"])
def update_profile():
    if "uid" not in session:
        return redirect(url_for("login"))
    changes = {}
    for field in EDITABLE:
        if field in request.form:
            changes[field] = request.form[field]
    if not changes:
        return redirect(url_for("profile"))
    assignments = ", ".join("%s = '%s'" % (k, v) for k, v in changes.items())
    db = get_db()
    db.execute("UPDATE users SET " + assignments + " WHERE id = ?", (session["uid"],))
    db.commit()
    return redirect(url_for("profile"))
