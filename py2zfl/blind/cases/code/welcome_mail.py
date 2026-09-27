from pathlib import Path

from flask import Flask, request
from jinja2 import Template

app = Flask(__name__)

TEMPLATE_PATH = Path(__file__).with_name("templates") / "welcome_mail.txt.j2"


@app.route("/mail/welcome", methods=["POST"])
def welcome_mail():
    source = TEMPLATE_PATH.read_text(encoding="utf-8")
    body = Template(source).render(
        user=request.form["username"],
        plan=request.form.get("plan", "free"),
    )
    return {"body": body}
