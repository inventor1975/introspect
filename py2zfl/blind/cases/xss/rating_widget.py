from flask import Flask, request
from markupsafe import Markup

app = Flask(__name__)


@app.route("/rating")
def rating():
    user = request.args.get("user", "")
    stars = request.args.get("stars", "")
    widget = Markup('<span class="stars" data-user="%s">%s</span>') % (user, stars)
    return widget
