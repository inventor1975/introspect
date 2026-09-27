import os

from flask import Flask, abort, request, send_file
from flask_login import current_user, login_required

app = Flask(__name__)

STATEMENTS = "/srv/bank/statements"


@app.route("/statements/open")
@login_required
def open_statement():
    name = request.args.get("file", "")
    if not name.lower().endswith(".pdf"):
        abort(400, "only PDF statements can be opened")
    base = os.path.join(STATEMENTS, str(current_user.id))
    return send_file(os.path.join(base, name), mimetype="application/pdf")
