from flask import Flask, request
import os
app = Flask(__name__)

@app.route('/run')
def run_view():
    cmd = request.args['cmd']       # source INSIDE the view
    os.system(cmd)                  # EXPECT: REFUTED [shell]

@app.route('/safe')
def safe_view():
    page = request.args.get('page')
    if page in ('a','b'):           # whitelist guard
        return render_template_string(page)   # EXPECT: EARNED (guarded)
    return "x"
