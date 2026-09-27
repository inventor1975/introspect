from flask import Blueprint, abort, render_template, request

from lib.storage import join_under

docs = Blueprint("docs", __name__, url_prefix="/help")
MANUAL_ROOT = "/srv/app/manuals"


@docs.route("/page")
def manual_page():
    page = request.args.get("page", "index.md")
    location = join_under(MANUAL_ROOT, page)
    try:
        with open(location, encoding="utf-8") as fh:
            markdown_source = fh.read()
    except OSError:
        abort(404)
    return render_template("manual.html", source=markdown_source, page=page)
