import uuid

from flask import Flask, request

app = Flask(__name__)


@app.route("/tickets/view")
def view_ticket():
    raw = request.args.get("id", "")
    try:
        ticket_id = uuid.UUID(raw)
    except ValueError:
        return "<p class='error'>That is not a valid ticket id.</p>", 400
    return f"<h1>Ticket {ticket_id}</h1><p>Status: open</p>"
