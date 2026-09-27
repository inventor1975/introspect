from flask import Flask, abort, render_template, request

from lib.db import get_connection

app = Flask(__name__)


@app.route("/catalog")
def catalog():
    sort = request.args.get("sort", "name")
    if not ("name" in sort or "price" in sort or "created" in sort):
        abort(400)
    conn = get_connection()
    products = conn.execute(
        f"SELECT id, name, price FROM products WHERE visible = 1 ORDER BY {sort}"
    ).fetchall()
    return render_template("catalog.html", products=products, sort=sort)
