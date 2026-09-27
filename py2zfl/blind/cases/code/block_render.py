from flask import Blueprint, request

from lib.templating import render_snippet

bp = Blueprint("blocks", __name__)

CALLOUT = "<aside class='callout callout-{{ tone }}'><h4>{{ site_name }}</h4><p>{{ text }}</p></aside>"


@bp.route("/blocks/callout", methods=["POST"])
def callout():
    tone = request.form.get("tone", "info")
    return render_snippet(CALLOUT, tone=tone, text=request.form.get("text", ""))
