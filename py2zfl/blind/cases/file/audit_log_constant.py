import datetime
import logging
import os

from flask import Flask, jsonify, request

app = Flask(__name__)
log = logging.getLogger(__name__)
AUDIT_DIR = "/var/log/app"
AUDIT_FILE = os.path.join(AUDIT_DIR, "downloads.audit")


@app.post("/audit/download")
def record_download():
    filename = request.form.get("filename", "")
    user = request.form.get("user", "anonymous")
    line = "%s\t%s\t%r\n" % (datetime.datetime.utcnow().isoformat(), user, filename)
    with open(AUDIT_FILE, "a", encoding="utf-8") as fh:
        fh.write(line)
    log.info("download recorded for %s", filename)
    return jsonify({"recorded": True})
