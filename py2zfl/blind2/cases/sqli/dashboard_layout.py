from flask import Flask, jsonify, request

from lib.db import get_db

app = Flask(__name__)


@app.route("/dashboard/widgets")
def widgets():
    layout = request.cookies.get("layout", "default")
    rows = get_db().execute(
        "SELECT widget, position FROM layouts WHERE name = '" + layout + "' ORDER BY position"
    ).fetchall()
    return jsonify([{"widget": r["widget"], "position": r["position"]} for r in rows])
