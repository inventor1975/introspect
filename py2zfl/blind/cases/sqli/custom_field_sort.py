import re

from flask import Flask, abort, jsonify, request

from lib.db import get_connection

app = Flask(__name__)
IDENT = re.compile(r"[a-z_][a-z0-9_]{0,30}")


@app.route("/api/contacts")
def contacts_sorted():
    field = request.args.get("order_by", "last_name")
    if IDENT.fullmatch(field) is None:
        abort(400, "bad order_by")
    conn = get_connection()
    rows = conn.execute(
        f"SELECT id, first_name, last_name, company FROM contacts ORDER BY {field} LIMIT 200"
    ).fetchall()
    return jsonify([dict(r) for r in rows])
