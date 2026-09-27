from flask import Flask, request
from flask_caching import Cache
from markupsafe import Markup

app = Flask(__name__)
cache = Cache(app, config={"CACHE_TYPE": "SimpleCache"})


@app.route("/sidebar", methods=["POST"])
def save_sidebar():
    cache.set("sidebar:" + request.form["user"], request.form["html"], timeout=3600)
    return "", 204


@app.route("/sidebar/<user>")
def sidebar(user):
    fragment = cache.get("sidebar:" + user) or ""
    return Markup('<aside class="sidebar">') + Markup(fragment) + Markup("</aside>")
