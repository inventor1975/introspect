from flask import Flask, Response, abort, request
from flask_login import current_user, login_required

from lib.storage_paths import member_file, read_bytes

app = Flask(__name__)


@app.route("/me/avatar")
@login_required
def my_avatar():
    image = request.args.get("img", "avatar.png")
    location = member_file(current_user.id, image)
    try:
        data = read_bytes(location)
    except FileNotFoundError:
        abort(404)
    return Response(data, mimetype="image/png")
