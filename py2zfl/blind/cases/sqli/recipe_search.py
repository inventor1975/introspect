from flask import Flask, render_template, request

from lib.db import get_connection
from lib.identifiers import escape_like

app = Flask(__name__)


@app.route("/recipes/search")
def recipe_search():
    term = escape_like(request.args.get("q", ""))
    conn = get_connection()
    recipes = conn.execute(
        "SELECT id, title FROM recipes WHERE title LIKE ? ESCAPE '\\' ORDER BY title",
        (f"%{term}%",),
    ).fetchall()
    return render_template("recipes/search.html", recipes=recipes)
