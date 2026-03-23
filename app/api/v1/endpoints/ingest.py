from app.services.orchestrate_pipeline_db import add_video
from app.schemas.models import VideoUploadResponse, JobStatusResponse
from app.core.exceptions import ProcessingError, VideoFormatError

from fastapi import APIRouter, UploadFile, File, BackgroundTasks, HTTPException
from uuid import uuid4
import shutil
import os

router = APIRouter()

# replace with DB later
jobs = {}


def run_pipeline(job_id: str, temp_path: str, temp_out_path: str, user_id: str):
    """Background task — runs the full video processing pipeline."""
    try:
        result = add_video.invoke({
            "video_path": temp_path,
            "output_dir": temp_out_path,
            "user_id": user_id
        })

        video_id = result["bucket_data"]["video_id"]

        jobs[job_id] = {
            "status": "completed",
            "video_id": video_id,
            "message": "Video processed and indexed successfully"
        }

    except Exception as e:
        print(str(e))
        jobs[job_id] = {
            "status": "failed",
            "video_id": None,
            "message": f"Processing failed: {str(e)}"
        }
        raise ProcessingError(f"Pipeline failed: {str(e)}")

    finally:
        # Cleanup temp files
        if os.path.isfile(temp_path):
            os.remove(temp_path)
        if os.path.isdir(temp_out_path):
            shutil.rmtree(temp_out_path)


@router.post("/upload", response_model=VideoUploadResponse)
def upload(USER_ID: str, file: UploadFile = File(...), background_tasks: BackgroundTasks = BackgroundTasks()):

    if not file.content_type or not file.content_type.startswith("video/"):
        raise VideoFormatError(f"File '{file.filename}' is not a valid video format. Got: {file.content_type}")


    job_id = str(uuid4())
    jobs[job_id] = {
        "status": "processing",
        "video_id": None,
        "message": "Video is being processed"
    }

    temp_path = f"/tmp/{file.filename}"
    temp_out_path = f"/tmp/{file.filename}_dir"
    os.makedirs(temp_out_path, exist_ok=True)

    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Kick off processing in background — returns immediately
    background_tasks.add_task(run_pipeline, job_id, temp_path, temp_out_path, USER_ID)

    return VideoUploadResponse(
        job_id=job_id,
        status="processing",
        message="Video received, processing started"
    )


@router.get("/get_status/{job_id}", response_model=JobStatusResponse)
def get_status(job_id: str):

    if job_id not in jobs:
        raise HTTPException(status_code=404, detail="Job ID not found")

    job = jobs[job_id]

    return JobStatusResponse(
        job_id=job_id,
        status=job["status"],
        video_id=job["video_id"],
        message=job["message"]
    )