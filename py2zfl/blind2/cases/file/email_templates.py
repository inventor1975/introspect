import os

from flask import Flask, abort, jsonify, request

app = Flask(__name__)

TEMPLATE_DIR = "/srv/mailer/templates"
ALLOWED_TEMPLATES = ("welcome.html", "reset.html", "digest.html", "invoice.html")


@app.route("/admin/mail-templates")
def mail_template():
    name = request.args.get("template", "")
    if name not in ALLOWED_TEMPLATES:
        abort(400, "unknown template")
    with open(os.path.join(TEMPLATE_DIR, name), encoding="utf-8") as fh:
        source = fh.read()
    return jsonify(template=name, source=source)
