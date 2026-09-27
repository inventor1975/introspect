from flask import Flask, jsonify, request

from lib.db import get_pg

app = Flask(__name__)


@app.route("/suppliers/contacts")
def supplier_contacts():
    name = request.args.get("name", "")
    conn = get_pg()
    cur = conn.cursor()
    stmt = cur.mogrify(
        "SELECT contact_name, email, phone FROM supplier_contacts WHERE supplier_name = %s",
        (name,),
    )
    cur.execute(stmt)
    rows = cur.fetchall()
    conn.close()
    return jsonify(rows)
