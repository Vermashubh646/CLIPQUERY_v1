from app.services.pinecone_integrate.pincone_initialize import vector_store

def get_retriever(user_id: str, max_results: int):
    search_filter = {
        "$or": [
            {"user_id": {"$eq": user_id}},
            {"public_listing": {"$eq": True}}
        ]
    }

    return vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={
            "k": max_results,
            "filter": search_filter
        }
    )

async def query_from_retriever(query: str, user_id: str, max_results: int):

    retriever = get_retriever(user_id, max_results)
    docs = retriever.invoke(query)

    return docs