from flask import Flask, request
from flask_login import current_user, login_required
from jinja2 import Template

app = Flask(__name__)


@app.post("/newsletter/preview")
@login_required
def preview_newsletter():
    body = request.form["body"]
    subject = request.form.get("subject", "(no subject)")
    template = Template(body)
    html = template.render(user=current_user, subject=subject)
    return {"subject": subject, "html": html}
