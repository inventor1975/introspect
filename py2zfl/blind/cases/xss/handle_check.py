from flask import Flask, abort, request

app = Flask(__name__)


@app.route("/handles/available")
def handle_available():
    handle = request.args.get("handle", "")
    if not handle or not handle.isalnum() or len(handle) > 30:
        abort(400)
    return f"<p>The handle <code>@{handle}</code> is available.</p>"
