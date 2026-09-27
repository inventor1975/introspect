import sqlite3

from flask import Flask, redirect, render_template, request, session, url_for

app = Flask(__name__)
app.secret_key = "workspace-dev-key"


def db():
    return sqlite3.connect("workspace.db")


@app.route("/login", methods=["POST"])
def login():
    conn = db()
    user = conn.execute(
        "SELECT id FROM users WHERE email = ? AND password_hash = ?",
        (request.form["email"], request.form["password_hash"]),
    ).fetchone()
    conn.close()
    if user is None:
        return render_template("login.html", error="Invalid credentials"), 401
    session["user_id"] = user[0]
    session["org_slug"] = request.form.get("org", "default")
    return redirect(url_for("workspace_docs"))


@app.route("/workspace/docs")
def workspace_docs():
    org = session.get("org_slug", "default")
    conn = db()
    docs = conn.execute(
        f"SELECT id, title, updated_at FROM documents WHERE org_slug = '{org}' ORDER BY updated_at DESC"
    ).fetchall()
    conn.close()
    return render_template("docs.html", docs=docs)
