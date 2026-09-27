from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route("/ops/migrate", methods=["POST"])
def run_migration_steps():
    lines = []
    for step in request.form.getlist("step"):
        step = step.rstrip()
        if not step or step.startswith("#"):
            continue
        lines.append(step)
    script = "\n".join(lines)
    scope = {"log": []}
    exec(script, scope)
    return jsonify(log=scope["log"], steps=len(lines))
