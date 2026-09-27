from flask import Flask, redirect, request, session, url_for

app = Flask(__name__)
app.secret_key = "change-me-in-production"


@app.route("/onboarding/finish")
def finish_onboarding():
    display = request.args.get("display_name", "").strip()[:64]
    if display:
        session["display_name"] = display
    return redirect(url_for("dashboard"))


@app.route("/dashboard")
def dashboard():
    who = session.get("display_name") or "there"
    return f"<h1>Welcome back, {who}</h1><div id='widgets'></div>"
