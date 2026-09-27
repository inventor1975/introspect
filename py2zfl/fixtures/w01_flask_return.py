from flask import Flask, request, jsonify
app = Flask(__name__)

@app.route("/hi/<name>")
def hi(name):
    return f"<h1>Hello {name}</h1>"          # EXPECT: REFUTED (a route variable returned as HTML)

@app.route("/n/<int:n>")
def num(n):
    return f"<p>{n}</p>"                     # clean: the <int:> converter

@app.route("/api")
def api():
    return {"q": request.args.get("q")}      # clean: a dict is JSON
