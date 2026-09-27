from flask import Flask, request
from markupsafe import Markup

from lib.textclean import collapse_ws, strip_script_tags

app = Flask(__name__)


@app.post("/bio/render")
def render_bio():
    raw = request.form.get("bio", "")
    cleaned = collapse_ws(strip_script_tags(raw))
    return Markup("<div class='bio'>") + Markup(cleaned) + Markup("</div>")
