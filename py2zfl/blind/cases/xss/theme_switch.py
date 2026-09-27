from flask import Flask, request

app = Flask(__name__)

THEMES = {
    "light": "/static/css/light.css",
    "dark": "/static/css/dark.css",
    "contrast": "/static/css/high-contrast.css",
}


@app.route("/preview-theme")
def preview_theme():
    requested = request.args.get("theme", "light")
    stylesheet = THEMES.get(requested, THEMES["light"])
    return (
        f'<html><head><link rel="stylesheet" href="{stylesheet}"></head>'
        "<body><p>Theme preview</p></body></html>"
    )
