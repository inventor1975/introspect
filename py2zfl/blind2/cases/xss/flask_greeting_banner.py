from flask import Flask, render_template_string, request
from markupsafe import Markup

app = Flask(__name__)

LAYOUT = """
<!doctype html>
<title>Welcome</title>
<div class="banner">{{ greeting }}</div>
<p>Thanks for stopping by.</p>
"""


@app.route("/welcome")
def welcome():
    name = request.args.get("name", "friend")
    greeting = Markup(f"<strong>Hello, {name}!</strong>")
    return render_template_string(LAYOUT, greeting=greeting)
