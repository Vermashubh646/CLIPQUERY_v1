from app.services.pinecone_integrate.pincone_initialize import vector_store

retriever = vector_store.as_retriever(search_type='similarity',search_kwargs={'k':4})

async def query_from_retriever(query : str):
    docs=retriever.invoke(query)

    return docs