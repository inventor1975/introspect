from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route("/reports/custom-column", methods=["POST"])
def custom_column():
    rows = [{"net": 100, "tax": 20}, {"net": 55, "tax": 11}]
    code = "for row in rows:\n    row['custom'] = "
    code += request.form["column_expr"]
    code += "\n"
    namespace = {"rows": rows}
    exec(code, namespace)
    return jsonify(namespace["rows"])
