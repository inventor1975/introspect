from flask import Flask, request
from jinja2 import BaseLoader, Environment

app = Flask(__name__)

env = Environment(loader=BaseLoader(), autoescape=False)
PLATE = env.from_string(
    "<div class='plate'><span>{{ first }}</span> <span>{{ last }}</span></div>"
)


@app.route("/plate")
def plate():
    return PLATE.render(
        first=request.args.get("first", ""),
        last=request.args.get("last", ""),
    )
