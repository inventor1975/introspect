from flask import Flask, request

app = Flask(__name__)

FIELDS = ("name", "email", "company", "phone")


@app.post("/contact/confirm")
def contact_confirm():
    entered = {}
    for field in FIELDS:
        value = request.form.get(field, "")
        if value:
            entered[field] = value
    rows = []
    for key, value in entered.items():
        rows.append(f"<tr><th>{key.capitalize()}</th><td>{value}</td></tr>")
    return "<table class='summary'>" + "".join(rows) + "</table>"
