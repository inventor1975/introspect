import os

from flask import Flask, request
from markupsafe import Markup, escape

app = Flask(__name__)

INTRO_PATH = os.path.join(app.root_path, "static", "help", "intro.html")


@app.route("/help")
def help_panel():
    topic = request.args.get("topic", "")
    with open(INTRO_PATH, encoding="utf-8") as fh:
        intro = Markup(fh.read())
    return Markup("<div class='help'>{}<p>No article for <em>{}</em> yet.</p></div>").format(
        intro, topic
    )
