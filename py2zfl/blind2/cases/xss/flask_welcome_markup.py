from flask import Flask, request
from markupsafe import Markup

app = Flask(__name__)


@app.route("/welcome-back")
def welcome_back():
    name = request.args.get("name", "friend")
    team = request.args.get("team", "")
    banner = Markup("<div class='banner'><strong>Hello, {}!</strong>{}</div>").format(
        name, Markup(" <em>({})</em>").format(team) if team else ""
    )
    return banner
