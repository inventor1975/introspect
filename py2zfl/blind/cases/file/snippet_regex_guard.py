import os
import re

from flask import Flask, abort, jsonify, request

app = Flask(__name__)
SNIPPET_DIR = os.path.join(os.path.dirname(__file__), "snippets")
NAME_RE = re.compile(r"[A-Za-z0-9_-]{1,64}")


@app.route("/api/snippet")
def snippet():
    name = request.args.get("name", "")
    if not NAME_RE.fullmatch(name):
        abort(400)
    with open(os.path.join(SNIPPET_DIR, name + ".py"), encoding="utf-8") as fh:
        return jsonify({"name": name, "code": fh.read()})
