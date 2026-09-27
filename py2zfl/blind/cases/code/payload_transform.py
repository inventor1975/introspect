from flask import Flask, jsonify, request

app = Flask(__name__)

TRANSFORM_SCRIPT = """
result = {
    "id": payload.get("id"),
    "email": (payload.get("email") or "").lower(),
    "tags": sorted(set(payload.get("tags", []))),
}
"""


@app.route("/ingest", methods=["POST"])
def ingest():
    scope = {"payload": request.get_json(force=True) or {}}
    exec(TRANSFORM_SCRIPT, scope)
    return jsonify(scope["result"])
