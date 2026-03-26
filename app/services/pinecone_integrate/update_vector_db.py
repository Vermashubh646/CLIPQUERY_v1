from langchain_core.documents import Document
from langchain_core.runnables import RunnableLambda
from uuid import uuid4

from app.services.pinecone_integrate.pincone_initialize import vector_store,pc
from app.core.exceptions import VectorDBError
from app.core.logger import custom_logger

def raw_data_to_documents(raw_data):
    documents = []

    for item in raw_data:
        documents.append(
            Document(
                page_content=item["clip_narrative"],
                metadata={
                    "video_name": item["video_name"],
                    "video_id": item["video_id"],        
                    "user_id": item["user_id"],        
                    "bucket": item["bucket"],           
                    "key": item["key"], 
                    "start_time": item["start_time"],
                    "end_time": item["end_time"],
                    "clip_narrative":item["clip_narrative"],
                    "public_listing":item["public_listing"]
                }
            )
        )
    uuids = [str(uuid4()) for _ in range(len(documents))]

    return documents, uuids

def pinecone_sink(output):
    try:

        raw_data = output["processed_json"]["raw_data"]

        documents, ids = raw_data_to_documents(raw_data)

        custom_logger.info("converted required text into langchain documents")
        vector_store.add_documents(
            documents=documents,
            ids=ids
        )
        
        custom_logger.info("Documents added to vector db successfully")
        return output  
    
    except Exception as e:

        raise VectorDBError(f"Failed to upload to Pinecone: {str(e)}")
    
add_to_pinecone=RunnableLambda(pinecone_sink)

def delete_indexes():
    pc.delete_index("clip-narratives")
