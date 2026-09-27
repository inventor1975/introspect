from flask import Flask, abort, request, send_from_directory

app = Flask(__name__)

MANUALS_DIR = "/srv/support/manuals"


@app.route("/support/manual")
def manual():
    name = request.args.get("name")
    if not name:
        abort(400)
    return send_from_directory(MANUALS_DIR, name, as_attachment=False)
