from flask import Flask, jsonify, request
from sqlalchemy import text

from lib.db import engine

app = Flask(__name__)

FIND_COUPON = text(
    "SELECT id, discount_pct FROM coupons WHERE code = :code AND redeemed_at IS NULL"
)
MARK_USED = text("UPDATE coupons SET redeemed_at = CURRENT_TIMESTAMP, redeemed_by = :user WHERE id = :id")


@app.route("/coupons/redeem", methods=["POST"])
def redeem():
    code = request.form["code"].strip().upper()
    user = request.form.get("user_id")
    with engine.begin() as conn:
        row = conn.execute(FIND_COUPON, {"code": code}).first()
        if row is None:
            return jsonify({"ok": False}), 404
        conn.execute(MARK_USED, {"user": user, "id": row.id})
    return jsonify({"ok": True, "discount": row.discount_pct})
