from flask import Blueprint, jsonify, request

from lib.db import get_connection
from lib.filters import build_where_clause

bp = Blueprint("segments", __name__, url_prefix="/segments")


@bp.route("/customers")
def customers_in_segment():
    filters = request.args.to_dict()
    filters.pop("page", None)
    sql = "SELECT id, name, city, tier FROM customers" + build_where_clause(filters)
    conn = get_connection()
    try:
        rows = conn.execute(sql).fetchall()
    finally:
        conn.close()
    return jsonify([dict(r) for r in rows])
