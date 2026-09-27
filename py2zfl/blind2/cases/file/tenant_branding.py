import os

from flask import Flask, abort, g, request, send_file

app = Flask(__name__)

TENANT_ROOT = "/srv/saas/tenants"


@app.before_request
def bind_tenant():
    g.tenant = request.headers.get("X-Tenant", "default")


@app.route("/branding/logo.png")
def tenant_logo():
    logo = os.path.join(TENANT_ROOT, g.tenant, "branding", "logo.png")
    if not os.path.isfile(logo):
        abort(404)
    return send_file(logo, mimetype="image/png")
