from flask import Flask, request

app = Flask(__name__)

THEMES = {"light", "dark", "sepia"}


@app.route("/settings/theme")
def theme():
    chosen = request.args.get("theme", "light")
    if chosen in THEMES:
        message = "Theme updated."
        css = chosen
    else:
        message = f"Unknown theme '{chosen}', keeping the default."
        css = "light"
    return f"<body class='theme-{css}'><p class='flash'>{message}</p></body>"
