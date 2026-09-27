import sqlite3

from flask import Flask, render_template, request

app = Flask(__name__)
ROLES = ("viewer", "editor", "admin", "owner")


@app.route("/team/members")
def members_by_role():
    role = request.args.get("role", "viewer")
    if role not in ROLES:
        role = "viewer"
    conn = sqlite3.connect("team.db")
    members = conn.execute(
        f"SELECT id, name, email FROM members WHERE role = '{role}' ORDER BY name"
    ).fetchall()
    conn.close()
    return render_template("members.html", members=members, role=role)
