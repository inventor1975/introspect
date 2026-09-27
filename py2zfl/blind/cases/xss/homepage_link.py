from flask import Flask, request
from markupsafe import escape

app = Flask(__name__)


@app.route("/u/card")
def user_card():
    website = request.args.get("website", "")
    nick = escape(request.args.get("nick", ""))
    return (
        f'<div class="card"><a href="{escape(website)}" rel="nofollow">{nick}</a>'
        "</div>"
    )
