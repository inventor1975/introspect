from fastapi import Request
import os
@app.get("/run")
async def run(request: Request):
    cmd = request.query_params["cmd"]   # Starlette/FastAPI source
    os.system(cmd)                      # EXPECT: REFUTED [shell]
