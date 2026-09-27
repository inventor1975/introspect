from flask import Flask, request

app = Flask(__name__)

THEMES = ("light", "dark", "high-contrast")


@app.route("/preview/theme")
def preview_theme():
    theme = request.args.get("theme", "light")
    if theme not in THEMES:
        theme = "light"
    return f"<body class='theme-{theme}'><h1>Preview</h1><p>Theme: {theme}</p></body>"
