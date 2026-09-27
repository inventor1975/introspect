from flask import Flask, jsonify, request

from lib.db import get_db
from lib.pagination import clamp_limit, page_offset

app = Flask(__name__)


@app.route("/activity")
def recent_activity():
    limit = clamp_limit(request.args.get("limit"))
    offset = page_offset(request.args.get("page"), limit)
    kind = request.args.get("kind", "comment")
    sql = f"SELECT id, kind, summary, at FROM activity WHERE kind = ? ORDER BY at DESC LIMIT {limit} OFFSET {offset}"
    rows = get_db().execute(sql, (kind,)).fetchall()
    return jsonify([dict(r) for r in rows])
