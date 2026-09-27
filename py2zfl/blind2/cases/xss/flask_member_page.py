import re

from flask import Flask, abort, request

app = Flask(__name__)

HANDLE_RE = re.compile(r"[A-Za-z0-9_]{1,32}")


@app.route("/members")
def member_page():
    handle = request.args.get("handle", "")
    if not HANDLE_RE.fullmatch(handle):
        abort(400)
    return f"<h1>@{handle}</h1><p>Joined recently.</p>"
