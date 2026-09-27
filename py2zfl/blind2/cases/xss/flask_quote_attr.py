import html

from flask import Flask, request

app = Flask(__name__)


@app.route("/toolbar")
def toolbar():
    tooltip = request.args.get("tip", "Save")
    safe_tip = html.escape(tooltip, quote=False)
    return (
        "<div class='toolbar'>"
        f"<button type='submit' title='{safe_tip}'>Save</button>"
        "</div>"
    )
