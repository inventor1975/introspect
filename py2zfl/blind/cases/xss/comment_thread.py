from flask import Flask, render_template, request
from markupsafe import Markup

app = Flask(__name__)


@app.route("/comments/preview", methods=["POST"])
def preview_comment():
    author = request.form.get("author", "anonymous")
    text = request.form["text"]
    rendered = Markup(text.replace("\n", "<br>"))
    return render_template("comment_preview.html", author=author, comment=rendered)
