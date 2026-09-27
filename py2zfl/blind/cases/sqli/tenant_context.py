from flask import Flask, g, jsonify, request

from lib.db import get_pg

app = Flask(__name__)


@app.before_request
def resolve_tenant():
    g.tenant_schema = "tenant_" + request.headers.get("X-Tenant", "public")


@app.route("/api/projects")
def list_projects():
    conn = get_pg()
    with conn, conn.cursor() as cur:
        cur.execute("SET LOCAL search_path TO " + g.tenant_schema)
        cur.execute("SELECT id, name, status FROM projects ORDER BY name")
        projects = cur.fetchall()
    return jsonify(projects)
