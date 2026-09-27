import os

from flask import Flask, request

app = Flask(__name__)
NOTES_DIR = "/srv/app/notes"


@app.route("/notes/raw")
def raw_note():
    try:
        note = request.args["note"]
    except KeyError:
        note = "welcome.txt"
    note_path = os.path.join(NOTES_DIR, note)
    with open(note_path, encoding="utf-8") as fh:
        return fh.read(), 200, {"Content-Type": "text/plain; charset=utf-8"}
