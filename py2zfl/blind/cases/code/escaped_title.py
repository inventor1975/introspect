from flask import Flask, request, render_template_string
from markupsafe import escape

app = Flask(__name__)

PAGE = "<html><head><title>{{ title }}</title></head><body>{{ body }}</body></html>"


@app.route("/preview")
def preview():
    title = escape(request.args.get("title", "Untitled"))
    body = escape(request.args.get("body", ""))
    return render_template_string(PAGE, title=title, body=body)
