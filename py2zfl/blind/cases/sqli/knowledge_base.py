import logging
import sqlite3

from flask import Flask, jsonify, request

app = Flask(__name__)
log = logging.getLogger("kb")

SEARCH_SQL = (
    "SELECT id, title, snippet(articles_fts, 1, '<b>', '</b>', '...', 12) "
    "FROM articles_fts WHERE articles_fts MATCH ? ORDER BY rank LIMIT 20"
)


@app.route("/kb/search")
def kb_search():
    term = request.args.get("q", "")
    trace = f"kb search q='{term}' ua={request.user_agent.string}"
    log.info(trace)
    conn = sqlite3.connect("kb.db")
    cur = conn.cursor()
    cur.execute(SEARCH_SQL, (term,))
    hits = cur.fetchall()
    conn.close()
    return jsonify({"query": term, "hits": hits})
