from flask import Flask, render_template, request

from lib.db import get_connection

app = Flask(__name__)


@app.route("/pricing")
def pricing():
    currency = request.cookies.get("currency", "usd").lower()
    conn = get_connection()
    plans = conn.execute(
        f"SELECT name, price_{currency} AS price, features FROM plans WHERE public = 1"
    ).fetchall()
    return render_template("pricing.html", plans=plans, currency=currency)
