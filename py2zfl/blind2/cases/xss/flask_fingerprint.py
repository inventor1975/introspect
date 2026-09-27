import hashlib

from flask import Flask, request

app = Flask(__name__)


@app.route("/avatar")
def avatar():
    email = request.args.get("email", "").strip().lower()
    digest = hashlib.md5(email.encode("utf-8")).hexdigest()
    return (
        f"<img class='avatar' alt='avatar' "
        f"src='https://www.gravatar.com/avatar/{digest}?s=80&d=identicon'>"
    )
