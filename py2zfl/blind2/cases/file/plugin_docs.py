from flask import Flask, abort, request, send_file
from werkzeug.utils import safe_join

app = Flask(__name__)

PLUGIN_DOCS = "/srv/marketplace/plugin-docs"


@app.route("/plugins/<plugin>/docs")
def plugin_doc(plugin):
    page = request.args.get("page", "README.md")
    path = safe_join(PLUGIN_DOCS, plugin, page)
    if path is None:
        abort(404)
    try:
        return send_file(path, mimetype="text/markdown")
    except FileNotFoundError:
        abort(404)
