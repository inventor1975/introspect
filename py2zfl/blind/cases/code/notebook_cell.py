import contextlib
import io

from fastapi import Body, FastAPI

app = FastAPI()


@app.post("/notebook/cell")
def run_cell(src: str = Body(..., embed=True), cell_id: str = Body("cell", embed=True)):
    code_obj = compile(source=src, filename=f"<{cell_id}>", mode="exec")
    stdout = io.StringIO()
    with contextlib.redirect_stdout(stdout):
        exec(code_obj, {})
    return {"cell": cell_id, "stdout": stdout.getvalue()}
