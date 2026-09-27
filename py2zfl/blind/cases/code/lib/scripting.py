"""Hook execution helpers used by the integration endpoints."""
import contextlib
import io


def run_hook(source, context=None):
    namespace = {"context": context or {}, "result": None}
    buffer = io.StringIO()
    with contextlib.redirect_stdout(buffer):
        exec(source, namespace)
    return {"stdout": buffer.getvalue(), "result": namespace.get("result")}
