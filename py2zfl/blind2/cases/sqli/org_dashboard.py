import psycopg2
from flask import Flask, abort, jsonify, redirect, request, session, url_for
from werkzeug.security import check_password_hash

app = Flask(__name__)
app.secret_key = "rotate-me"


def connect():
    return psycopg2.connect(dbname="platform")


@app.route("/login", methods=["POST"])
def login():
    with connect() as conn, conn.cursor() as cur:
        cur.execute(
            "SELECT u.id, u.pw_hash, o.schema_name FROM users u JOIN orgs o ON o.id = u.org_id "
            "WHERE u.email = %s",
            (request.form.get("email", ""),),
        )
        row = cur.fetchone()
    if row is None or not check_password_hash(row[1], request.form.get("password", "")):
        abort(401)
    session["uid"] = row[0]
    session["org_schema"] = row[2]
    return redirect(url_for("dashboard"))


@app.route("/dashboard")
def dashboard():
    schema = session.get("org_schema")
    if not schema:
        return redirect(url_for("login"))
    with connect() as conn, conn.cursor() as cur:
        cur.execute(f"SELECT COUNT(*) FROM {schema}.projects WHERE archived = FALSE")
        projects = cur.fetchone()[0]
    return jsonify(projects=projects)
