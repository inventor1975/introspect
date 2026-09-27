from flask import Blueprint, current_app, request, send_file

legal = Blueprint("legal", __name__)


@legal.route("/legal/terms.pdf")
def terms_pdf():
    inline = request.args.get("inline") == "1"
    path = current_app.config["TERMS_PDF_PATH"]
    return send_file(path, mimetype="application/pdf", as_attachment=not inline)
