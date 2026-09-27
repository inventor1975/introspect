import os
import shutil

from flask import Flask, abort, jsonify, request

app = Flask(__name__)


class FileOperations:
    root = "/srv/app/userfiles"

    def _full(self, rel):
        return os.path.join(self.root, rel)

    def op_stat(self, rel):
        st = os.stat(self._full(rel))
        return {"size": st.st_size, "mtime": st.st_mtime}

    def op_delete(self, rel):
        os.remove(self._full(rel))
        return {"deleted": rel}

    def op_archive(self, rel):
        shutil.move(self._full(rel), os.path.join(self.root, ".archive"))
        return {"archived": rel}


ops = FileOperations()


@app.post("/files/<action>")
def file_action(action):
    handler = getattr(ops, "op_" + action, None)
    if handler is None:
        abort(404)
    return jsonify(handler(request.form["path"]))
