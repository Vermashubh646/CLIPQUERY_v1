from .pincone_initialize import vector_store,pc
from langchain_core.documents import Document
from langchain_core.runnables import RunnableLambda
from uuid import uuid4

def raw_data_to_documents(raw_data):
    documents = []

    for item in raw_data:
        documents.append(
            Document(
                page_content=item["clip_narrative"],
                metadata={
                    "video_name": item["video_name"],
                    "video_id": item["video_id"],        
                    "bucket": item["bucket"],           
                    "key": item["key"], 
                    "start_time": item["start_time"],
                    "end_time": item["end_time"],
                    "clip_narrative":item["clip_narrative"]
                }
            )
        )
    uuids = [str(uuid4()) for _ in range(len(documents))]

    return documents, uuids

def pinecone_sink(output):
    raw_data = output["processed_json"]["raw_data"]

    documents, ids = raw_data_to_documents(raw_data)

    print("converted required text into langchain documents")

    vector_store.add_documents(
        documents=documents,
        ids=ids
    )
    
    print("Documents added to vector db successfully")

    return output  

add_to_pinecone=RunnableLambda(pinecone_sink)

def delete_indexes():
    pc.delete_index("clip-narratives")
