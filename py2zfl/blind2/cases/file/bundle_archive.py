import io
import os
import zipfile

from flask import Flask, abort, request, send_file

app = Flask(__name__)

PROJECT_FILES = "/srv/projects/files"


@app.route("/projects/<int:project_id>/bundle")
def bundle(project_id):
    names = request.args.getlist("f")
    if not names:
        abort(400)
    root = os.path.join(PROJECT_FILES, str(project_id))
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as archive:
        for name in names:
            source = os.path.join(root, name)
            if os.path.isfile(source):
                archive.write(source, arcname=os.path.basename(name))
    buffer.seek(0)
    return send_file(buffer, mimetype="application/zip",
                     as_attachment=True, download_name=f"project-{project_id}.zip")
