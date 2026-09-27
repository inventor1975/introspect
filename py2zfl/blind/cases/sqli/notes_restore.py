import sqlite3

from flask import Flask, flash, redirect, request, url_for
from flask_login import login_required

app = Flask(__name__)
app.secret_key = "change-me"


@app.route("/notes/restore", methods=["POST"])
@login_required
def restore_notes():
    upload = request.files.get("backup")
    if upload is None or not upload.filename.endswith(".sql"):
        flash("Please choose a .sql backup file.")
        return redirect(url_for("restore_notes"))
    script = upload.read().decode("utf-8")
    conn = sqlite3.connect("notes.db")
    conn.executescript(script)
    conn.close()
    flash("Notes restored.")
    return redirect("/notes")
