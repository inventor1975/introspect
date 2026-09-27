from flask import Flask, jsonify, request

app = Flask(__name__)
DRAFTS_ROOT = "/srv/app/drafts"


@app.post("/drafts/save")
def save_draft():
    data = request.form
    target = DRAFTS_ROOT
    target += "/" + data.get("folder", "inbox")
    target += "/" + data.get("title", "untitled") + ".md"
    with open(target, "w", encoding="utf-8") as fh:
        fh.write(data.get("body", ""))
    return jsonify({"saved": True})
