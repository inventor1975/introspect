import re

from flask import Flask, request, render_template_string

app = Flask(__name__)

_TEMPLATE_CHARS = re.compile(r"[{}%#]")


def strip_template_syntax(value):
    return _TEMPLATE_CHARS.sub("", value)


@app.route("/profile/hello")
def hello():
    display = strip_template_syntax(request.args.get("display_name", "there"))
    page = f"<h1>Hello {display}</h1><p>Last login: {{{{ last_login }}}}</p>"
    return render_template_string(page, last_login="yesterday")
