import json

from flask import Flask, jsonify, request

app = Flask(__name__)

FALLBACK_LOCALE = "en"


class Catalog:
    def __init__(self, base):
        self.base = base

    def path_for(self, locale):
        return "{}/{}/messages.json".format(self.base, locale)

    def load(self, locale):
        with open(self.path_for(locale), encoding="utf-8") as fh:
            return json.load(fh)


catalog = Catalog("i18n")


@app.route("/api/messages")
def messages():
    locale = request.headers.get("X-Locale") or FALLBACK_LOCALE
    try:
        data = catalog.load(locale)
    except FileNotFoundError:
        data = catalog.load(FALLBACK_LOCALE)
    return jsonify(data)
