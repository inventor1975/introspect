from flask import Flask, request

app = Flask(__name__)

CATEGORY_LABELS = {
    "hw": "Hardware",
    "sw": "Software",
    "svc": "Services",
}


@app.route("/browse")
def browse():
    key = request.args.get("cat", "hw")
    label = CATEGORY_LABELS.get(key, "All categories")
    return f"<nav class='crumbs'>Home &rsaquo; <b>{label}</b></nav>"
