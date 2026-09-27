import logging

from flask import Flask, request
from markupsafe import escape

app = Flask(__name__)
log = logging.getLogger(__name__)


@app.route("/nickname")
def nickname():
    nick = request.args.get("nick", "")
    log.info("nickname lookup: %r", nick)
    if len(nick) > 40:
        nick = nick[:40]
    nick = escape(nick)
    return f"<p>Your nickname is <b>{nick}</b></p>"
