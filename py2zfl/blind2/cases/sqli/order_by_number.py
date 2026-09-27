import re

import MySQLdb
from flask import Flask, abort, jsonify, request

app = Flask(__name__)
ORDER_NO = re.compile(r"[0-9]{6,12}")


@app.route("/orders/by-number")
def order_by_number():
    number = request.args.get("n", "")
    if not ORDER_NO.fullmatch(number):
        abort(400)
    conn = MySQLdb.connect(host="localhost", user="web", db="shop")
    cur = conn.cursor()
    cur.execute("SELECT id, status, total FROM orders WHERE order_no = '%s'" % number)
    row = cur.fetchone()
    conn.close()
    if row is None:
        abort(404)
    return jsonify(id=row[0], status=row[1], total=float(row[2]))
