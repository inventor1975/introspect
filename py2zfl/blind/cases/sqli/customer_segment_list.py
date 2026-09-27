from flask import Blueprint, jsonify, request

from lib.db import get_connection
from lib.filters import build_param_where

bp = Blueprint("segment_list", __name__, url_prefix="/segments")
SEGMENT_COLUMNS = ("city", "tier", "country", "newsletter")


@bp.route("/list")
def segment_list():
    clause, params = build_param_where(request.args, SEGMENT_COLUMNS)
    conn = get_connection()
    try:
        rows = conn.execute("SELECT id, name, city, tier FROM customers" + clause, params).fetchall()
    finally:
        conn.close()
    return jsonify([dict(r) for r in rows])
