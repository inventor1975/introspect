import sqlite3

from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route("/support/ticket")
def ticket_status():
    ticket = request.args.get("id", "")
    if not ticket.isdigit():
        return jsonify({"error": "ticket id must be numeric"}), 400
    conn = sqlite3.connect("helpdesk.db")
    row = conn.execute(
        "SELECT id, subject, status, updated_at FROM tickets WHERE id = " + ticket
    ).fetchone()
    conn.close()
    if row is None:
        return jsonify({"error": "not found"}), 404
    return jsonify(dict(zip(("id", "subject", "status", "updated_at"), row)))
