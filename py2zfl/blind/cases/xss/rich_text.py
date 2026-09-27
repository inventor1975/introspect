import bleach
from flask import Flask, render_template, request
from markupsafe import Markup

app = Flask(__name__)

ALLOWED_TAGS = {"b", "i", "em", "strong", "a", "p", "ul", "ol", "li", "code"}
ALLOWED_ATTRS = {"a": ["href", "title"]}


@app.route("/posts/preview", methods=["POST"])
def post_preview():
    raw = request.form.get("body", "")
    clean = bleach.clean(
        raw,
        tags=ALLOWED_TAGS,
        attributes=ALLOWED_ATTRS,
        protocols={"http", "https", "mailto"},
        strip=True,
    )
    return render_template("post_preview.html", body=Markup(clean))
