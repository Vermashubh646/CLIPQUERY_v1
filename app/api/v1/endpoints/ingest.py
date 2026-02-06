from app.services.orchestrate_pipeline_db import add_video
from fastapi import APIRouter, UploadFile, File
import shutil
import os

router = APIRouter()

@router.post("/upload")
async def upload(USER_ID: str,file: UploadFile = File(...)):
    temp_path = f"/tmp/{file.filename}"
    temp_out_path = f"/tmp/{file.filename}_dir"

    os.makedirs(temp_out_path, exist_ok=True)

    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    result = add_video.invoke({
        "video_path":temp_path,
        "output_dir":temp_out_path,
        "user_id":USER_ID})

    os.remove(temp_path)
    os.remove(temp_out_path)

    return result
