import os

import MySQLdb
from flask import Flask, abort, jsonify

app = Flask(__name__)


def db():
    return MySQLdb.connect(
        host="localhost", user="web", passwd=os.environ.get("DB_PASS", ""), db="club"
    )


@app.route("/members/<username>")
def member(username):
    conn = db()
    cur = conn.cursor()
    cur.execute("SELECT id, username, joined FROM members WHERE username = '%s'" % username)
    row = cur.fetchone()
    conn.close()
    if not row:
        abort(404)
    return jsonify(id=row[0], username=row[1], joined=str(row[2]))
