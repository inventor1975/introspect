from flask import Flask, Response, request

app = Flask(__name__)

BLOCKED = ("<script>", "</script>", "javascript:")


def strip_scripts(value):
    for token in BLOCKED:
        value = value.replace(token, "")
    return value


@app.route("/guestbook/preview", methods=["POST"])
def guestbook_preview():
    entry = strip_scripts(request.form.get("entry", ""))
    return Response("<div class='entry'>" + entry + "</div>", mimetype="text/html")
