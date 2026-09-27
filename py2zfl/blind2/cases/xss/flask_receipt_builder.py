from flask import Flask, request
from markupsafe import escape

app = Flask(__name__)


class ReceiptHtml:
    def __init__(self, number):
        self.number = number
        self.lines = []

    def add_line(self, description, amount):
        self.lines.append((escape(description), float(amount)))

    def render(self):
        body = "".join(
            f"<tr><td>{d}</td><td class='num'>{a:.2f}</td></tr>" for d, a in self.lines
        )
        return f"<h1>Receipt {self.number}</h1><table>{body}</table>"


@app.route("/receipt/preview", methods=["POST"])
def receipt_preview():
    receipt = ReceiptHtml(number="PREVIEW")
    for d, a in zip(request.form.getlist("desc"), request.form.getlist("amount", type=float)):
        receipt.add_line(d, a)
    return receipt.render()
