# core/exceptions.py

class VideoFormatError(Exception):
    """Raised when uploaded file is not a supported video format."""
    pass

class ProcessingError(Exception):
    """Raised when the video processing pipeline fails."""
    pass

class StorageError(Exception):
    """Raised when S3 upload/delete fails."""
    pass

class VectorDBError(Exception):
    """Raised when Pinecone operations fail."""
    pass