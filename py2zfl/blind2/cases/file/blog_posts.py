import os
import re

import markdown
from flask import Flask, abort, render_template_string, request

app = Flask(__name__)

POSTS_DIR = "/srv/blog/posts"
SLUG = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")


@app.route("/blog")
def post():
    slug = request.args.get("post", "")
    if len(slug) > 80 or not SLUG.fullmatch(slug):
        abort(404)
    path = os.path.join(POSTS_DIR, slug + ".md")
    try:
        with open(path, encoding="utf-8") as fh:
            html = markdown.markdown(fh.read())
    except FileNotFoundError:
        abort(404)
    return render_template_string("<article>{{ body|safe }}</article>", body=html)
