from flask import Blueprint, request

from lib.templating import render_snippet

bp = Blueprint("cms", __name__)


@bp.route("/cms/blocks/preview", methods=["POST"])
def preview_block():
    block_source = request.form.get("snippet", "")
    return render_snippet(block_source, page_title=request.form.get("page_title", ""))
