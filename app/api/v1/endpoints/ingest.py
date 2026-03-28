from app.services.orchestrate_pipeline_db import add_video
from app.schemas.models import VideoUploadResponse, JobStatusResponse
from app.core.exceptions import VideoFormatError
from app.tasks.pipeline_task import run_pipeline
from app.core.logger import custom_logger

from fastapi import APIRouter, UploadFile, File, HTTPException
from celery.result import AsyncResult
from celery import states
from uuid import uuid4
import shutil
import os

router = APIRouter()

def check_size_limit(file: UploadFile):

    file.file.seek(0, 2)
    size = file.file.tell()
    file.file.seek(0)
    
    if size > (50*1024*1024):
        raise HTTPException(status_code=413, detail="File size exceeds the 50MB limit.")
    

@router.post("/upload", response_model=VideoUploadResponse)
def upload(USER_ID: str,public_listing: bool ,file: UploadFile = File(...)):

    check_size_limit(file)

    if not file.content_type or not file.content_type.startswith("video/"):
        raise VideoFormatError(f"File '{file.filename}' is not a valid video format. Got: {file.content_type}")


    job_id = str(uuid4())

    temp_path = f"/tmp/{file.filename}"
    temp_out_path = f"/tmp/{file.filename}_dir"
    os.makedirs(temp_out_path, exist_ok=True)

    try:
        
        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

    except Exception as e:
        if os.path.exists(temp_path):
            os.remove(temp_path)
        if os.path.exists(temp_out_path):
            os.rmdir(temp_out_path)
        raise HTTPException(status_code=500, detail=f"Failed to save upload: {str(e)}")

    # Kick off processing in background — returns immediately
    task = run_pipeline.delay(job_id, temp_path, temp_out_path, USER_ID, public_listing)
    
    return VideoUploadResponse(
        job_id=job_id,
        status="processing",
        message="Video received, processing started"
    )


@router.get("/get_status/{job_id}", response_model=JobStatusResponse)
def get_status(job_id: str):

    task_result = AsyncResult(job_id)

    if task_result.state == states.PENDING and task_result.date_done is None:
        raise HTTPException(status_code=404, detail="Job ID not found")

    if task_result.state == 'PENDING':
        return JobStatusResponse(job_id=job_id, status="processing", video_id=None, message="Still in queue...")
    elif task_result.state == 'SUCCESS':
        return JobStatusResponse(job_id=job_id, status="completed", video_id=task_result.result["video_id"], message="Done!")
    elif task_result.state == 'FAILURE':
        info = task_result.info
        if isinstance(info, dict):
            error_msg = info.get("message", "An unknown error occurred.")
        else:
            error_msg = str(info)  # Raw exception → convert to string
        return JobStatusResponse(job_id=job_id, status="failed", video_id=None, message=error_msg)
