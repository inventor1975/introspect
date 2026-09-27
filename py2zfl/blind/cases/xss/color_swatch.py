from flask import Flask, request

app = Flask(__name__)

PALETTE = ("red", "green", "blue", "teal", "orange")


@app.route("/swatch")
def swatch():
    color = request.args.get("color", "teal")
    if color in PALETTE:
        return f'<div class="swatch" style="background:{color}">{color}</div>'
    return "<p>Unknown colour</p>", 400
