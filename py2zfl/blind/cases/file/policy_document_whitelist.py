import os

from flask import Flask, abort, request, send_file

app = Flask(__name__)
POLICY_DIR = "/srv/app/policies"
PUBLISHED = ("privacy.pdf", "terms.pdf", "cookies.pdf", "accessibility.pdf")


@app.route("/legal")
def legal_document():
    doc = request.args.get("doc", "terms.pdf")
    if doc not in PUBLISHED:
        abort(404)
    return send_file(os.path.join(POLICY_DIR, doc), mimetype="application/pdf")
