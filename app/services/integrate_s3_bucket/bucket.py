import boto3
import uuid
from langchain_core.runnables import RunnableLambda

s3 = boto3.client("s3", region_name="us-east-1")

BUCKET_NAME = "clipquerybucket"

def upload_video(file_data: dict):
    video_id = str(uuid.uuid4())
    ext = file_data["video_path"].split(".")[-1]

    object_key = f"videos/{file_data['user_id']}/{video_id}.{ext}"

    s3.upload_file(
        file_data["video_path"],
        BUCKET_NAME,
        object_key,
        ExtraArgs={
            "ContentType": "video/mp4"
        }
    )

    return {
        "video_id": video_id,
        "bucket": BUCKET_NAME,
        "key": object_key,
        "s3_uri": f"s3://{BUCKET_NAME}/{object_key}"
    }

upload_to_bucket=RunnableLambda(upload_video)

def delete_video(file_data: dict):
    s3.delete_object(
        Bucket=file_data["bucket"],
        Key=file_data['key']
    )
    print(f"Video {file_data['key']} deleted")

    return file_data

delete_from_bucket=RunnableLambda(delete_video)
