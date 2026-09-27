from flask import Flask, request

app = Flask(__name__)


@app.route("/hello")
def hello():
    name = request.args.get("name", "friend")
    return f"<html><body><h1>Hello, {name}!</h1></body></html>"
