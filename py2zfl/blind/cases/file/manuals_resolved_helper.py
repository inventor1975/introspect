from flask import Blueprint, abort, render_template, request

from lib.storage import resolve_inside

manuals = Blueprint("manuals", __name__, url_prefix="/manuals")
MANUAL_ROOT = "/srv/app/manuals"


@manuals.route("/page")
def manual_page():
    page = request.args.get("page", "index.md")
    try:
        location = resolve_inside(MANUAL_ROOT, page)
    except ValueError:
        abort(404)
    try:
        with open(location, encoding="utf-8") as fh:
            source = fh.read()
    except OSError:
        abort(404)
    return render_template("manual.html", source=source, page=page)
