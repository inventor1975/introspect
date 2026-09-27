import os

from flask import Flask, request

app = Flask(__name__)
TERMS_DIR = os.path.join(app.root_path, "legal")
TERMS_BY_LANG = {
    "en": "terms_en.html",
    "de": "terms_de.html",
    "es": "terms_es.html",
}


def _load(path):
    with open(path, encoding="utf-8") as fh:
        return fh.read()


@app.route("/terms")
def terms():
    lang = request.args.get("lang", "en")
    filename = TERMS_BY_LANG.get(lang, TERMS_BY_LANG["en"])
    return _load(os.path.join(TERMS_DIR, filename))
