from flask import Flask, jsonify, redirect, request, session, url_for

app = Flask(__name__)
app.secret_key = "change-me"


@app.route("/budget/formula", methods=["POST"])
def store_formula():
    session["budget_formula"] = request.form["formula"]
    return redirect(url_for("budget_summary"))


@app.route("/budget")
def budget_summary():
    income, spend = 5200.0, 3100.0
    formula = session.get("budget_formula", "income - spend")
    return jsonify(remaining=eval(formula, {"income": income, "spend": spend}))
