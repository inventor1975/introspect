import sqlite3

from flask import Flask, g, render_template, request

app = Flask(__name__)


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect("recipes.db")
    return g.db


@app.route("/recipes/by-tags")
def recipes_by_tags():
    tags = [t.strip().lower() for t in request.args.getlist("tag") if t.strip()]
    if not tags:
        return render_template("recipes/list.html", recipes=[])
    in_list = ", ".join(f"'{t}'" for t in tags)
    sql = (
        "SELECT r.id, r.title FROM recipes r JOIN recipe_tags rt ON rt.recipe_id = r.id "
        f"WHERE rt.tag IN ({in_list}) GROUP BY r.id HAVING COUNT(*) = {len(tags)}"
    )
    recipes = get_db().execute(sql).fetchall()
    return render_template("recipes/list.html", recipes=recipes)
