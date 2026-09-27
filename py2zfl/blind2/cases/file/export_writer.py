from pathlib import Path

from flask import Flask, jsonify, request

app = Flask(__name__)

EXPORT_ROOT = Path("/srv/reporting/exports")


@app.post("/api/exports")
def write_export():
    payload = request.get_json(force=True) or {}
    target = payload.get("target", "export.csv")
    content = payload.get("content", "")
    destination = Path(EXPORT_ROOT, target)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(content, encoding="utf-8")
    return jsonify(written=str(destination), size=len(content)), 201
