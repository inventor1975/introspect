from flask import Flask

app = Flask(__name__)

ARTICLES = {
    "python": ["Generators in depth", "Typing tips"],
    "rust": ["Ownership primer"],
}


@app.route("/tag/<tag>")
def tag_archive(tag):
    titles = ARTICLES.get(tag.lower(), [])
    listing = "".join(f"<li>{t}</li>" for t in titles) or "<li>No articles yet</li>"
    return f"<h1>Articles tagged “{tag}”</h1><ul>{listing}</ul>"
