import psycopg2
from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/vendors")
def vendor_search():
    term = request.args.get("q", "")
    conn = psycopg2.connect("dbname=procurement")
    cur = conn.cursor()
    cur.execute(
        "SELECT id, name, category FROM vendors WHERE name ILIKE %s ORDER BY name LIMIT 50",
        ("%%%s%%" % term,),
    )
    vendors = cur.fetchall()
    conn.close()
    return render_template("vendors.html", vendors=vendors, q=term)
