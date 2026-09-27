import os
import uuid

from fastapi import FastAPI, File, HTTPException, UploadFile

app = FastAPI()

PHOTO_DIR = "/srv/gallery/incoming"
IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp"}


@app.post("/photos")
async def upload_photo(photo: UploadFile = File(...)):
    original = photo.filename or ""
    extension = os.path.splitext(original)[1].lower()
    if extension not in IMAGE_EXTENSIONS:
        raise HTTPException(status_code=415, detail=f"unsupported file {original}")
    stored_name = f"{uuid.uuid4().hex}{extension}"
    destination = os.path.join(PHOTO_DIR, stored_name)
    with open(destination, "wb") as out:
        out.write(await photo.read())
    return {"id": stored_name, "original": original}
