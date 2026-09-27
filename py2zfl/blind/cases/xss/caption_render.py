from flask import Flask, request
from jinja2 import BaseLoader, Environment

app = Flask(__name__)

env = Environment(loader=BaseLoader(), autoescape=True)
CAPTION = env.from_string(
    "<figure><img src='/static/{{ image|urlencode }}'><figcaption>{{ text }}</figcaption></figure>"
)


@app.route("/caption")
def caption():
    return CAPTION.render(
        image=request.args.get("image", "placeholder.png"),
        text=request.args.get("text", ""),
    )
