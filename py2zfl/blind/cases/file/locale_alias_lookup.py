import json
import os

from flask import Flask, jsonify, request

app = Flask(__name__)
LOCALE_DIR = os.path.join(app.root_path, "locales")
ALIASES = {
    "en": "en_US",
    "de": "de_DE",
    "fr": "fr_FR",
    "pt": "pt_BR",
}


@app.route("/i18n/messages")
def messages():
    requested = request.args.get("lang", "en")
    locale_name = ALIASES.get(requested, requested)
    with open(os.path.join(LOCALE_DIR, locale_name + ".json"), encoding="utf-8") as fh:
        catalog = json.load(fh)
    return jsonify(catalog)
