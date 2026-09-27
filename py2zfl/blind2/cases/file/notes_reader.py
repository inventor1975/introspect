import os

from flask import Flask, abort, jsonify, request

app = Flask(__name__)

NOTES_DIR = "/srv/notes"


def read_note(name):
    if ".." in name:
        raise PermissionError(name)
    with open(os.path.join(NOTES_DIR, name), encoding="utf-8") as fh:
        return fh.read()


@app.route("/api/notes")
def get_note():
    name = request.args.get("note", "")
    try:
        body = read_note(name)
    except PermissionError:
        abort(403)
    except FileNotFoundError:
        abort(404)
    return jsonify(note=name, body=body)
