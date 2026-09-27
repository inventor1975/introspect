from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://stores@localhost/stores"
db = SQLAlchemy(app)


@app.route("/stores")
def store_locator():
    city = request.args.get("city")
    open_sunday = request.args.get("sunday") == "1"
    stmt = "SELECT name, address, phone FROM stores WHERE active"
    if city:
        stmt += " AND city = '" + city + "'"
    if open_sunday:
        stmt += " AND opens_sunday"
    stores = db.session.execute(text(stmt)).mappings().all()
    return render_template("stores.html", stores=stores)
