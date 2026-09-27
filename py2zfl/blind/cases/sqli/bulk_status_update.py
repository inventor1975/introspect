import sqlite3

from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route("/api/tickets/close", methods=["POST"])
def close_tickets():
    payload = request.get_json(force=True)
    ids = payload.get("ids") or []
    if not ids:
        return jsonify({"closed": 0})
    id_list = ",".join(str(i) for i in ids)
    conn = sqlite3.connect("helpdesk.db")
    cur = conn.execute(f"UPDATE tickets SET status = 'closed' WHERE id IN ({id_list})")
    conn.commit()
    closed = cur.rowcount
    conn.close()
    return jsonify({"closed": closed})
