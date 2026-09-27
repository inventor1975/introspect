from flask import Flask, request

from lib.fragments import render_tile

app = Flask(__name__)


@app.route("/widgets/tile")
def tile():
    label = request.args.get("label", "Visitors")
    value = request.args.get("value", "0")
    return render_tile(label, value)
