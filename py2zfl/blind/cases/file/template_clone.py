import os
import shutil
import uuid

from flask import Flask, jsonify, request

app = Flask(__name__)
TEMPLATE_DIR = "/srv/app/templates/email"
DRAFTS_DIR = "/srv/app/drafts"


@app.post("/api/drafts")
def create_draft_from_template():
    payload = request.get_json(force=True)
    template_name = payload.get("template", "blank.html")
    source = TEMPLATE_DIR + "/" + template_name
    draft_id = uuid.uuid4().hex
    destination = os.path.join(DRAFTS_DIR, draft_id + ".html")
    shutil.copyfile(source, destination)
    return jsonify({"draft": draft_id}), 201
