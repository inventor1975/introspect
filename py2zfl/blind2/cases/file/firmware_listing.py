import os

from flask import Flask, abort, request, send_file

app = Flask(__name__)

FIRMWARE_DIR = "/srv/devices/firmware"


@app.route("/firmware")
def firmware():
    wanted = request.args.get("image", "")
    for entry in os.listdir(FIRMWARE_DIR):
        if entry == wanted:
            return send_file(os.path.join(FIRMWARE_DIR, entry), as_attachment=True)
    abort(404)
