from flask import Flask, jsonify, request

from lib.db import get_db

app = Flask(__name__)


@app.route("/coupons/redeem", methods=["POST"])
def redeem():
    code = request.form.get("code", "")
    if request.form.get("mode") == "numeric":
        code = str(int(code))
    else:
        code = code.strip().upper()
    db = get_db()
    row = db.execute(
        "SELECT id, discount FROM coupons WHERE code = '%s' AND redeemed = 0" % code
    ).fetchone()
    if row is None:
        return jsonify(ok=False), 404
    db.execute("UPDATE coupons SET redeemed = 1 WHERE id = ?", (row["id"],))
    db.commit()
    return jsonify(ok=True, discount=row["discount"])
