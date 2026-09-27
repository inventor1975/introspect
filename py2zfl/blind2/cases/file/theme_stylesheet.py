from flask import Flask, Response, request

app = Flask(__name__)

DEFAULT_THEME = "light"


def load_css(theme):
    with open(f"static/themes/{theme}.css", encoding="utf-8") as fh:
        return fh.read()


@app.route("/theme.css")
def theme_css():
    theme = request.cookies.get("theme", DEFAULT_THEME)
    try:
        body = load_css(theme)
    except OSError:
        body = load_css(DEFAULT_THEME)
    return Response(body, mimetype="text/css")
