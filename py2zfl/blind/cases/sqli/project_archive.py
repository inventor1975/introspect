import sqlite3

from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/projects")
def project_list():
    include_archived = request.args.get("archived") == "1"
    owner = request.args.get("owner")
    sql = "SELECT id, name, owner, archived FROM projects WHERE 1 = 1"
    params = []
    if not include_archived:
        sql += " AND archived = 0"
    if owner:
        sql += " AND owner = ?"
        params.append(owner)
    conn = sqlite3.connect("projects.db")
    projects = conn.execute(sql + " ORDER BY name", params).fetchall()
    conn.close()
    return render_template("projects.html", projects=projects)
