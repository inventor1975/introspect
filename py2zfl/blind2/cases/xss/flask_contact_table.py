from flask import Flask, request
from markupsafe import Markup, escape

app = Flask(__name__)

FIELDS = ("name", "email", "company", "phone")


@app.post("/contact/review")
def contact_review():
    rows = []
    for field in FIELDS:
        value = request.form.get(field, "")
        if not value:
            continue
        rows.append(Markup("<tr><th>{}</th><td>{}</td></tr>").format(field.capitalize(), value))
    table = Markup("<table class='summary'>") + Markup("").join(rows) + Markup("</table>")
    return str(table)
