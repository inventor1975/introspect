from flask import Flask, jsonify, request

app = Flask(__name__)

REPORT_SRC = """
total = sum(r['amount'] for r in rows)
count = len(rows)
average = total / count if count else 0
"""


@app.route("/reports/summary")
def summary():
    report_name = request.args.get("name", "summary")
    code = compile(REPORT_SRC, filename=f"<report:{report_name}>", mode="exec")
    ns = {"rows": [{"amount": 10}, {"amount": 32}]}
    exec(code, ns)
    return jsonify(name=report_name, total=ns["total"], average=ns["average"])
