import os

from flask import Flask, flash, redirect, request, url_for

app = Flask(__name__)
app.config["AVATAR_FOLDER"] = "/srv/app/static/avatars"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.post("/account/avatar")
def upload_avatar():
    upload = request.files.get("avatar")
    if upload is None or upload.filename == "":
        flash("No file selected")
        return redirect(url_for("account"))
    if not allowed_file(upload.filename):
        flash("Unsupported image type")
        return redirect(url_for("account"))
    target = os.path.join(app.config["AVATAR_FOLDER"], upload.filename)
    upload.save(target)
    flash("Avatar updated")
    return redirect(url_for("account"))
