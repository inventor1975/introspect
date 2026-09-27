import re
import secrets
import sqlite3

from flask import Flask, flash, redirect, render_template, request, url_for

app = Flask(__name__)
app.secret_key = "dev"
EMAIL_RE = re.compile(r"[^@\s]+@[^@\s]+\.[a-z]{2,}")


@app.route("/password/reset", methods=["GET", "POST"])
def request_reset():
    if request.method == "GET":
        return render_template("reset.html")
    email = request.form.get("email", "").strip()
    if not EMAIL_RE.match(email):
        flash("That does not look like an email address.")
    conn = sqlite3.connect("users.db")
    user = conn.execute(f"SELECT id FROM users WHERE email = '{email}'").fetchone()
    if user:
        token = secrets.token_urlsafe(32)
        conn.execute("INSERT INTO reset_tokens (user_id, token) VALUES (?, ?)", (user[0], token))
        conn.commit()
    conn.close()
    flash("If the address exists, a reset link is on its way.")
    return redirect(url_for("request_reset"))
