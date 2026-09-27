from flask import Flask, make_response, request

app = Flask(__name__)


@app.post("/profile/preview")
def preview_profile():
    display = request.form.get("display_name", "Anonymous")
    bio = request.form["bio"]
    body = "<div class='profile'>"
    body += "<h1>" + display.title() + "</h1>"
    body += "<div class='bio'>" + bio + "</div>"
    body += "</div>"
    resp = make_response(body)
    resp.headers["Cache-Control"] = "no-store"
    return resp
