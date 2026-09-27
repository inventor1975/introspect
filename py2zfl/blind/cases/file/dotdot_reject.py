import os

from flask import Flask, abort, request, send_file

app = Flask(__name__)
FIRMWARE_DIR = "/srv/firmware"


@app.route("/firmware")
def firmware_image():
    image = request.args.get("image", "")
    if not image or ".." in image or os.path.isabs(image) or "\\" in image:
        abort(400)
    path = os.path.join(FIRMWARE_DIR, image)
    if not os.path.isfile(path):
        abort(404)
    return send_file(path, mimetype="application/octet-stream")
