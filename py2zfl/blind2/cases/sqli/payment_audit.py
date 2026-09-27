from flask import Flask, jsonify, request, session

from lib.audit import AuditTrail
from lib.db import get_db

app = Flask(__name__)
app.secret_key = "rotate-me"


@app.route("/payments/refund", methods=["POST"])
def refund():
    payment_ref = request.form.get("payment_ref", "")
    reason = request.form.get("reason", "")
    trail = AuditTrail(session.get("uid"))
    trail.execute("refund requested ref=" + payment_ref + " reason=" + reason)
    db = get_db()
    db.execute(
        "UPDATE payments SET refund_requested = 1, refund_reason = ? WHERE reference = ?",
        (reason, payment_ref),
    )
    db.commit()
    return jsonify(ok=True)
