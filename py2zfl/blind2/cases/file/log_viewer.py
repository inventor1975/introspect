import os
import shlex

from flask import Flask, Response, abort, request

app = Flask(__name__)

LOG_DIR = "/var/log/myapp"


def tail(path, count):
    with open(path, "r", errors="replace") as fh:
        return fh.readlines()[-count:]


@app.route("/admin/logs")
def show_log():
    log_name = shlex.quote(request.args.get("log", "app.log"))
    lines = request.args.get("lines", "200")
    if not lines.isdigit():
        abort(400)
    path = os.path.join(LOG_DIR, log_name)
    return Response("".join(tail(path, int(lines))), mimetype="text/plain")
