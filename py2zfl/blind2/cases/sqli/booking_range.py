import sqlite3

from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route("/bookings/range")
def booking_range():
    start, end = request.args.get("from", ""), request.args.get("to", "")
    room = request.args.get("room", type=int)
    sql = "SELECT id, room, starts_at FROM bookings WHERE starts_at BETWEEN '%s' AND '%s'" % (start, end)
    args = ()
    if room is not None:
        sql += " AND room = ?"
        args = (room,)
    with sqlite3.connect("bookings.db") as conn:
        rows = conn.execute(sql, args).fetchall()
    return jsonify([{"id": r[0], "room": r[1], "starts_at": r[2]} for r in rows])
