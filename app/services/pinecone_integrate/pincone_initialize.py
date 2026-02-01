from pinecone import Pinecone,ServerlessSpec
from langchain_pinecone import PineconeVectorStore
from langchain_huggingface import HuggingFaceEndpointEmbeddings
import os

pc = Pinecone()

index_name = "clip-narratives"

# Create index if it doesn't exist
if not pc.has_index(index_name):
    pc.create_index(
        name=index_name,
        dimension=4096,
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region="us-east-1")
    )

index = pc.Index(index_name)

embeddings = HuggingFaceEndpointEmbeddings(
    model="Qwen/Qwen3-Embedding-8B",
    huggingfacehub_api_token=os.getenv("HUGGINGFACEHUB_ACCESS_TOKEN")
)

vector_store = PineconeVectorStore(index=index, embedding=embeddings)
