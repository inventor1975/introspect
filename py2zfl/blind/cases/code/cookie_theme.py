from flask import Flask, make_response, request, render_template_string

app = Flask(__name__)

DEFAULT_THEME = "body { background: #fff; color: #222; }"


@app.route("/dashboard")
def dashboard():
    theme = request.cookies.get("theme_css", DEFAULT_THEME)
    page = (
        "<html><head><style>" + theme + "</style></head>"
        "<body><h1>{{ heading }}</h1></body></html>"
    )
    return render_template_string(page, heading="Your dashboard")


@app.route("/theme", methods=["POST"])
def set_theme():
    resp = make_response("", 204)
    resp.set_cookie("theme_css", request.form.get("css", DEFAULT_THEME))
    return resp
