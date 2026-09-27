import psycopg2
from flask import Flask, abort, jsonify, request

from lib.accounts import accounts_with_status, fetch_account

app = Flask(__name__)


def connect():
    return psycopg2.connect(dbname="accounts")


@app.route("/admin/accounts/lookup")
def account_lookup():
    email = request.args.get("email", "")
    conn = connect()
    try:
        account = fetch_account(conn, email)
        suspended = accounts_with_status(conn, "suspended")
    finally:
        conn.close()
    if account is None:
        abort(404)
    return jsonify(
        id=account[0],
        email=account[1],
        name=account[2],
        suspended_peers=len(suspended),
    )
