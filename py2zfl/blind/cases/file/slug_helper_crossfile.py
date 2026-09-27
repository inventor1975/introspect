import os

from flask import Flask, jsonify, request

from lib.naming import slugify_name

app = Flask(__name__)
BOARD_DIR = "/srv/app/boards"


@app.post("/boards")
def save_board():
    title = request.form.get("title", "")
    filename = slugify_name(title) + ".json"
    with open(os.path.join(BOARD_DIR, filename), "w", encoding="utf-8") as fh:
        fh.write(request.form.get("content", "{}"))
    return jsonify({"file": filename}), 201
