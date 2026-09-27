import sqlite3

from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route("/glossary")
def glossary_lookup():
    term = request.args.get("term", "")
    conn = sqlite3.connect("glossary.db")
    row = conn.execute(_lookup_sql(term)).fetchone()
    conn.close()
    return jsonify({"term": term, "definition": row[0] if row else None})


def _lookup_sql(term):
    sql = f"SELECT definition FROM glossary WHERE term = '{term}'"
    if len(term) <= 64:
        return sql
    term = term[:64].replace("'", "''")
    return f"SELECT definition FROM glossary WHERE term = '{term}'"
