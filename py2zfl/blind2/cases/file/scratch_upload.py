import tempfile

from fastapi import FastAPI, Header, UploadFile

app = FastAPI()

SCRATCH = "/var/tmp/scratch"


@app.post("/scratch")
async def store_scratch(file: UploadFile, x_client_tag: str = Header("anon")):
    data = await file.read()
    with tempfile.NamedTemporaryFile(prefix=f"{x_client_tag}_", suffix=".bin",
                                     dir=SCRATCH, delete=False) as tmp:
        tmp.write(data)
        stored = tmp.name
    return {"stored": stored, "bytes": len(data)}
