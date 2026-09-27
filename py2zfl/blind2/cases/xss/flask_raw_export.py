from flask import Flask, Response, request

app = Flask(__name__)


@app.route("/export/snippet")
def export_snippet():
    body = request.args.get("body", "")
    title = request.args.get("title", "snippet")
    content = f"<h1>{title}</h1>\n<div>{body}</div>\n"
    resp = Response(content, mimetype="text/plain")
    resp.headers["X-Content-Type-Options"] = "nosniff"
    resp.headers["Content-Disposition"] = "attachment; filename=snippet.html.txt"
    return resp
