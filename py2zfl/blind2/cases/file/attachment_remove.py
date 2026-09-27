import os

from flask import Blueprint, abort, jsonify, request

bp = Blueprint("attachments", __name__, url_prefix="/tickets")

ATTACHMENT_ROOT = "/srv/helpdesk/attachments"


@bp.route("/<int:ticket_id>/attachments", methods=["DELETE"])
def remove_attachment(ticket_id):
    attachment = request.form.get("attachment", "")
    folder = os.path.join(ATTACHMENT_ROOT, str(ticket_id))
    target = os.path.join(folder, attachment)
    if not os.path.exists(target):
        abort(404)
    os.remove(target)
    return jsonify(ticket=ticket_id, removed=attachment)
