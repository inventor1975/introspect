import os

from flask import Flask, request, render_template_string

app = Flask(__name__)

DEFAULT_BANNER = "<div class='banner'>Hi {{ user }}, welcome back.</div>"


@app.route("/banner")
def banner():
    source = os.environ.get("BANNER_TEMPLATE", DEFAULT_BANNER)
    return render_template_string(source, user=request.args.get("user", "guest"))
