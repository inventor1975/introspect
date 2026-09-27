from flask import Flask, make_response

app = Flask(__name__)

PAGES = {
    "install": "<h1>Installation</h1><p>Run the installer.</p>",
    "usage": "<h1>Usage</h1><p>Open the app.</p>",
}


@app.route("/docs/<path:page>")
def docs(page):
    content = PAGES.get(page)
    if content is None:
        return make_response(f"<h1>Not found</h1><p>No documentation page named {page}.</p>", 404)
    return content
