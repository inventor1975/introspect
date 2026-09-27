from flask import Flask, jsonify, request

app = Flask(__name__)

NET_EXPR = "sum(line['amount'] for line in lines)"
GROSS_EXPR = "sum(line['amount'] * (1 + line['vat']) for line in lines)"


@app.route("/invoices/total")
def invoice_total():
    lines = [{"amount": 100.0, "vat": 0.2}, {"amount": 40.0, "vat": 0.1}]
    if request.args.get("mode") == "net":
        expr = NET_EXPR
    else:
        expr = GROSS_EXPR
    return jsonify(mode=request.args.get("mode", "gross"), total=eval(expr, {"lines": lines, "sum": sum}))
