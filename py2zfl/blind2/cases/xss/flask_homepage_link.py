from flask import Flask, request
from markupsafe import escape

app = Flask(__name__)


@app.route("/members/<int:member_id>/links")
def member_links(member_id):
    site = request.args.get("website", "")
    label = request.args.get("label", "Homepage")
    link = f'<a rel="nofollow" href="{escape(site)}">{escape(label)}</a>'
    return f"<p>Member {member_id}: {link}</p>"
