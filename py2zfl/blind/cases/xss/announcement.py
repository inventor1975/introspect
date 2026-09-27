from flask import Flask, request

app = Flask(__name__)


@app.route("/announce")
def announce():
    headline = request.args.get("headline", "")
    return _wrap_announcement(headline)


def _wrap_announcement(text):
    return '<div class="announcement" role="alert">' + text + "</div>"
