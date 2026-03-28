from app.core.celery_app import celery_worker
from app.services.orchestrate_pipeline_db import add_video
from app.core.logger import custom_logger

from celery.exceptions import Ignore

@celery_worker.task(bind=True)
def run_pipeline(self, job_id: str, temp_path: str, temp_out_path: str, user_id: str, public_listing: bool):
    """Background task — runs the full video processing pipeline."""
    try:
        result = add_video.invoke({
            "video_path": temp_path,
            "output_dir": temp_out_path,
            "user_id": user_id,
            "public_listing": public_listing
        })

        video_id = result["bucket_data"]["video_id"]

        return {"video_id": video_id, "message": "Video processed and indexed successfully!"}

    except Exception as e:

        self.update_state(state='FAILURE', meta={"message": str(e)})
        custom_logger.error(f"Pipeline crashed for job {job_id}", exc_info=True)

        raise Ignore()
