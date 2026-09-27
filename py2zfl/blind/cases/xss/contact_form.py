from flask import Flask, make_response, request

app = Flask(__name__)

FIELDS = ("name", "email", "subject", "message")


@app.route("/contact/confirm", methods=["POST"])
def confirm():
    submitted = {}
    for field in FIELDS:
        submitted[field] = request.form.get(field, "")
    rows = []
    for key in FIELDS:
        rows.append("<dt>%s</dt><dd>%s</dd>" % (key.capitalize(), submitted[key]))
    return make_response("<h2>Please confirm</h2><dl>" + "".join(rows) + "</dl>")
