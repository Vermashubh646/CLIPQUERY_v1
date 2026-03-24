from pydantic import BaseModel, Field
from typing import Annotated, Optional, Literal, List

# VideoUploadResponse`, `SearchQuery`, `SearchResult`, `ClipResult`

class VideoUploadResponse(BaseModel):
    job_id: Annotated[str, Field(
        title="Job ID",
        description="Unique ID to track this upload/processing job"
    )]
    status: Annotated[Literal["processing"], Field(
        title="Upload Status",
        description="Will always be 'processing' at upload time"
    )]
    message: Annotated[str, Field(
        description="Response message about the upload"
    )]


class JobStatusResponse(BaseModel):
    job_id: Annotated[str, Field(
        title="Job ID"
    )]
    status: Annotated[Literal["processing", "completed", "failed"], Field(
        title="Job Status",
        description="Current status of the processing job"
    )]
    video_id: Annotated[Optional[str], Field(
        default=None,
        title="Video ID",
        description="Video ID in S3 bucket. Only available when status is 'completed'"
    )]
    message: Annotated[str, Field(
        description="Status details"
    )]


class SearchQuery(BaseModel):
    query: Annotated[str, Field(title="Input Query")]
    user_id: Annotated[str, Field(title="User Id")]
    max_results: Annotated[int, Field(default=5, title="Max Results")]

class ClipResult(BaseModel):
    video_name: str
    start_time: float
    end_time: float
    narrative: str
    video_url: str
    score: float

class SearchResponse(BaseModel):
    results: list[ClipResult]
             