import psycopg2
from flask import Flask, g, jsonify, request

app = Flask(__name__)
DSN = "dbname=saas user=saas"


@app.before_request
def bind_tenant():
    tenant = request.headers.get("X-Tenant", "public")
    g.conn = psycopg2.connect(DSN)
    with g.conn.cursor() as cur:
        cur.execute("SET search_path TO %s, public" % tenant)


@app.teardown_request
def release(exc):
    conn = g.pop("conn", None)
    if conn is not None:
        conn.close()


@app.route("/projects")
def projects():
    with g.conn.cursor() as cur:
        cur.execute("SELECT id, name FROM projects ORDER BY name")
        return jsonify([{"id": r[0], "name": r[1]} for r in cur.fetchall()])
