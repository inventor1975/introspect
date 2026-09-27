from flask import Flask, jsonify, request

app = Flask(__name__)

STAFF = {"ana": "Support", "ben": "Billing"}


@app.route("/api/staff")
def staff_lookup():
    who = request.args.get("who", "")
    team = STAFF.get(who.lower())
    if team is None:
        return jsonify(error=f"<b>{who}</b> not found"), 404
    return jsonify(name=who, team=team, html=f"<span class='team'>{who}</span>")
