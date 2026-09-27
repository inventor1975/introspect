import html

from flask import Flask, request

app = Flask(__name__)


@app.route("/tools/evaluate", methods=["POST"])
def evaluate():
    expression = html.escape(request.form.get("expression", ""))
    result = eval(expression)
    return f"<p>{expression} = {html.escape(str(result))}</p>"
