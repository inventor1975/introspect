import sqlite3

from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route("/workspaces", methods=["POST"])
def create_workspace():
    workspace = request.form.get("workspace", "").strip().lower()
    owner = request.form.get("owner", "")
    if not workspace:
        return jsonify(error="workspace required"), 400
    conn = sqlite3.connect("notes.db")
    conn.executescript(
        f"""
        CREATE TABLE IF NOT EXISTS notes_{workspace} (
            id INTEGER PRIMARY KEY,
            body TEXT NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        );
        INSERT INTO workspace_owners (workspace, owner) VALUES ('{workspace}', '{owner}');
        """
    )
    conn.close()
    return jsonify(created=workspace), 201
