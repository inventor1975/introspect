import html
from flask import Flask, request, render_template_string
from jinja2 import Environment
from markupsafe import Markup
app = Flask(__name__)
env = Environment(autoescape=False)
PAGE = "<p>{{ bio|safe }}</p>"

@app.route("/a")
def a():
    return env.from_string("<p>{{ v }}</p>").render(v=request.args["x"])        # EXPECT: REFUTED (autoescape off)

@app.route("/b")
def b():
    return render_template_string(PAGE, bio=request.args["x"])                  # EXPECT: REFUTED (|safe)

@app.route("/c")
def c():
    return f"<span title='{html.escape(request.args['x'], quote=False)}'>i</span>"   # EXPECT: REFUTED

@app.route("/d")
def d():
    return Markup("<b>{}</b>").format(request.args["x"])                        # clean: Markup.format escapes

@app.route("/e")
def e():
    return render_template_string("<p>{{ v }}</p>", v=request.args["x"])        # clean: autoescaped
