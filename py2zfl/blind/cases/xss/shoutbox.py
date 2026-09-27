from collections import deque

from flask import Flask, redirect, request, url_for

app = Flask(__name__)

RECENT = deque(maxlen=50)


@app.route("/shout", methods=["POST"])
def shout():
    RECENT.appendleft((request.form.get("nick", "anon"), request.form.get("text", "")))
    return redirect(url_for("board"))


@app.route("/board")
def board():
    items = []
    for nick, text in RECENT:
        items.append("<li><b>%s</b>: %s</li>" % (nick, text))
    return "<ul class='shouts'>" + "".join(items) + "</ul>"
