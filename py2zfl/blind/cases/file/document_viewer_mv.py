import os

from flask import Flask, abort, request, send_file
from flask.views import MethodView

app = Flask(__name__)


class DocumentView(MethodView):
    storage_root = "/data/documents"

    def get(self):
        self.requested = request.args.get("doc", "")
        if not self.requested:
            abort(400)
        self.resolved = os.path.join(self.storage_root, self.requested)
        return self._stream()

    def _stream(self):
        if not os.path.exists(self.resolved):
            abort(404)
        return send_file(self.resolved)


app.add_url_rule("/documents/view", view_func=DocumentView.as_view("document_view"))
