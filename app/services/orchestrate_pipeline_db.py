from .pinecone_integrate.update_vector_db import add_to_pinecone
from .processor_final_data import ultimate_video_pipe

add_video = ultimate_video_pipe | add_to_pinecone