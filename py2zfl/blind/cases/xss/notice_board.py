from flask import Flask, request
from markupsafe import escape

app = Flask(__name__)


@app.route("/notice")
def notice():
    msg = request.args.get("msg", "")
    level = request.args.get("level", "info")
    if level == "info":
        msg = escape(msg)
    elif level == "warning":
        msg = f"<b>Warning:</b> {escape(msg)}"
    return f'<div class="notice notice-{escape(level)}">{msg}</div>'
