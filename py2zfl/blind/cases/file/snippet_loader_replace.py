import os

from flask import Flask, jsonify, request

app = Flask(__name__)
SNIPPET_DIR = os.path.join(os.path.dirname(__file__), "snippets")


def strip_traversal(value):
    return value.replace("../", "").replace("..\\", "")


@app.route("/api/snippets")
def load_snippet():
    raw = request.args.get("name", "")
    name = strip_traversal(raw)
    with open(os.path.join(SNIPPET_DIR, name), encoding="utf-8") as fh:
        code = fh.read()
    return jsonify({"name": name, "code": code})
