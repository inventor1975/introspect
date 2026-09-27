from flask import Flask, request
from markupsafe import Markup

app = Flask(__name__)


@app.route("/mention")
def mention():
    username = request.args.get("user", "")
    link = Markup('<a class="mention" href="/u/{0}">@{0}</a>').format(username)
    return "<p>Mentioned: " + str(link) + "</p>"
