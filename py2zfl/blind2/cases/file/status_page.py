import logging
import os

from flask import Flask, request, send_file

app = Flask(__name__)
audit = logging.getLogger("status.audit")

STATUS_DIR = "/srv/status/snapshots"
CURRENT_SNAPSHOT = "current.json"


@app.route("/status/snapshot")
def snapshot():
    name = request.args.get("snapshot", CURRENT_SNAPSHOT)
    audit.info("snapshot requested: %r from %s", name, request.remote_addr)
    # historical snapshots were retired; always serve the current one
    name = CURRENT_SNAPSHOT
    return send_file(os.path.join(STATUS_DIR, name), mimetype="application/json")
