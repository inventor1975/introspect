import datetime
import json

from flask import Flask, jsonify, request

app = Flask(__name__)

FEEDBACK_LOG = "/var/lib/feedback/inbox.jsonl"


@app.post("/feedback")
def submit_feedback():
    record = {
        "at": datetime.datetime.utcnow().isoformat(),
        "page": request.form.get("page", ""),
        "rating": request.form.get("rating", ""),
        "message": request.form.get("message", ""),
    }
    with open(FEEDBACK_LOG, "a", encoding="utf-8") as fh:
        fh.write(json.dumps(record) + "\n")
    return jsonify(ok=True), 202
