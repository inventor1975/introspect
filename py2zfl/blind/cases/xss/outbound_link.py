from urllib.parse import urlparse

from flask import Flask, abort, request
from markupsafe import escape

app = Flask(__name__)


@app.route("/leaving")
def leaving():
    url = request.args.get("url", "")
    parsed = urlparse(url)
    if parsed.scheme not in ("http", "https") or not parsed.netloc:
        abort(400)
    return (
        "<p>You are leaving this site.</p>"
        f'<a href="{escape(url)}" rel="noopener">Continue to {escape(parsed.netloc)}</a>'
    )
