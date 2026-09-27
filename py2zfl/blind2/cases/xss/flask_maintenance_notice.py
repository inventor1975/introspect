import os

from flask import Flask, render_template_string, request
from markupsafe import Markup

app = Flask(__name__)

NOTICE_PATH = os.path.join(os.path.dirname(__file__), "content", "maintenance.html")

STATUS = """
<h1>Service status</h1>
<div class="notice">{{ notice }}</div>
<p>Region: {{ region }}</p>
"""


@app.route("/status")
def status():
    with open(NOTICE_PATH, encoding="utf-8") as fh:
        notice = Markup(fh.read())
    return render_template_string(STATUS, notice=notice, region=request.args.get("region", "eu"))
