import sqlite3

from flask import Flask, abort, render_template, request

app = Flask(__name__)
ALLOWED_SORT = ("last_name", "first_name", "department", "hired_on")


@app.route("/people")
def employee_directory():
    col = request.args.get("sort", "last_name")
    if col not in ALLOWED_SORT:
        abort(400)
    direction = "DESC" if request.args.get("desc") else "ASC"
    conn = sqlite3.connect("hr.db")
    people = conn.execute(
        f"SELECT first_name, last_name, department, hired_on FROM employees "
        f"ORDER BY {col} {direction}"
    ).fetchall()
    conn.close()
    return render_template("people.html", people=people, sort=col)
