from flask import Flask, request, render_template_string
from markupsafe import escape

app = Flask(__name__)

LAYOUT = """<!doctype html>
<title>{{ title }}</title>
<div class="banner">%s</div>
{%% for item in items %%}<li>{{ item }}</li>{%% endfor %%}
"""


@app.route("/promo")
def promo():
    message = escape(request.args.get("msg", "Welcome!"))
    page = LAYOUT % message
    return render_template_string(page, title="Promotions", items=["Spring sale", "Free shipping"])
