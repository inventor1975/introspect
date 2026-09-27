import sqlite3
from collections import deque

from flask import Flask, jsonify, request

app = Flask(__name__)


class JobQueue:
    """In-process queue of named report jobs, drained by a worker thread."""

    def __init__(self):
        self._pending = deque()

    def execute(self, job_name, **options):
        self._pending.append((job_name, options))
        return len(self._pending)


queue = JobQueue()


@app.route("/reports/run", methods=["POST"])
def run_report():
    job = request.form["job"]
    position = queue.execute(job, requested_by=request.form.get("user"))
    conn = sqlite3.connect("reports.db")
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO report_requests (job, requested_by, position) VALUES (?, ?, ?)",
        (job, request.form.get("user"), position),
    )
    conn.commit()
    conn.close()
    return jsonify({"queued": job, "position": position})
