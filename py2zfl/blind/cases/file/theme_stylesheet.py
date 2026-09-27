from flask import Flask, Response, request

app = Flask(__name__)
DEFAULT_THEME = "light.css"


@app.route("/assets/theme.css")
def theme_css():
    theme = request.cookies.get("theme", DEFAULT_THEME)
    css_file = f"{app.root_path}/themes/{theme}"
    with open(css_file, encoding="utf-8") as fh:
        body = fh.read()
    resp = Response(body, mimetype="text/css")
    resp.headers["Cache-Control"] = "public, max-age=600"
    return resp
