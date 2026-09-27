from flask import Flask, request, render_template_string

app = Flask(__name__)

WELCOME = """<html><body>
<h1>Welcome, {{ name }}!</h1>
{% if ref %}<p>You were referred by {{ ref }}.</p>{% endif %}
</body></html>"""


@app.route("/welcome")
def welcome():
    name = request.args.get("name", "guest")
    ref = request.args.get("ref")
    return render_template_string(WELCOME, name=name, ref=ref)
