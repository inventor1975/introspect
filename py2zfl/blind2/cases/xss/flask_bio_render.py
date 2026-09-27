import bleach
from flask import Flask, request
from markupsafe import Markup

app = Flask(__name__)

ALLOWED_TAGS = ["b", "i", "em", "strong", "p", "br"]


@app.post("/bio/preview")
def bio_preview():
    raw = request.form.get("bio", "")
    cleaned = bleach.clean(raw, tags=ALLOWED_TAGS, attributes={}, strip=True)
    return Markup("<div class='bio'>") + Markup(cleaned) + Markup("</div>")
