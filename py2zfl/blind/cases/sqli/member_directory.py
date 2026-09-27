import MySQLdb
from flask import Flask, render_template, request

app = Flask(__name__)


def db():
    return MySQLdb.connect(host="localhost", user="club", passwd="club", db="club")


def _quote(value):
    return value.replace('"', '\\"')


@app.route("/members")
def member_directory():
    surname = _quote(request.args.get("surname", ""))
    conn = db()
    cur = conn.cursor()
    cur.execute(
        "SELECT first_name, surname, joined FROM members WHERE surname LIKE '" + surname + "%' "
        "ORDER BY surname, first_name"
    )
    members = cur.fetchall()
    conn.close()
    return render_template("members.html", members=members)
