from flask import Flask, request, render_template_string

app = Flask(__name__)


@app.route("/card")
def greeting_card():
    recipient = request.args.get("to", "friend")
    occasion = request.args.get("occasion", "birthday")
    page = f"""
    <html><body>
      <div class="card">
        <h1>Happy {occasion}, {recipient}!</h1>
        <p>From all of us at {{{{ company }}}}</p>
      </div>
    </body></html>
    """
    return render_template_string(page, company="Acme Cards")
