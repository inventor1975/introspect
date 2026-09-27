from flask import Flask, request

app = Flask(__name__)


class InvoiceHtml:
    def __init__(self, number):
        self.number = number
        self.lines = []

    def add_line(self, description, amount):
        self.lines.append((description, amount))

    def render(self):
        body = "".join(
            f"<tr><td>{d}</td><td class='num'>{a:.2f}</td></tr>" for d, a in self.lines
        )
        return f"<h1>Invoice {self.number}</h1><table>{body}</table>"


@app.route("/invoice/draft", methods=["POST"])
def invoice_draft():
    inv = InvoiceHtml(number="DRAFT")
    descriptions = request.form.getlist("desc")
    amounts = request.form.getlist("amount", type=float)
    for d, a in zip(descriptions, amounts):
        inv.add_line(d, a)
    return inv.render()
