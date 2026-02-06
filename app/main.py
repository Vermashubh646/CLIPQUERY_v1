import os
import json
from dotenv import load_dotenv

load_dotenv('.env')

from services.pinecone_integrate.update_vector_db import add_to_pinecone, delete_indexes
from services.processor_final_data import ultimate_video_pipe,json_processing_pipe,update_json_pipe
from services.orchestrate_pipeline_db import add_video

input_video = "../Videos/"
output_path="../Outputs/"
file_name="Regeneration in Action ｜ Building Resilient Farms in Iowa ｜ National Geographic.mp4"
base_name =os.path.splitext(file_name)[0]
out_path=os.path.join(output_path,base_name)
USER_ID=56985

data = add_video.invoke({"video_path":os.path.join(input_video,file_name),"output_dir":out_path,"user_id":USER_ID})

with open("data.json",'w') as f:
    json.dump(data["updated_data"], f, indent=2)

# delete_indexes()

# data=ultimate_video_pipe.invoke({"video_path":os.path.join(input_video,file_name),"output_dir":out_path})

# with open("/home/kamadahanam/Documents/ALL_WORKS/CLIPQUERY_UPGRADED/Outputs/Improving Mindsets & Lives During Health Challenges ｜ Limitless： Live Better Now ｜ Nat Geo/Improving Mindsets & Lives During Health Challenges ｜ Limitless： Live Better Now ｜ Nat Geo_complete_transcript.txt","r") as f:
#     d = f.read()

# with open("/home/kamadahanam/Documents/ALL_WORKS/CLIPQUERY_UPGRADED/Outputs/Improving Mindsets & Lives During Health Challenges ｜ Limitless： Live Better Now ｜ Nat Geo/Improving Mindsets & Lives During Health Challenges ｜ Limitless： Live Better Now ｜ Nat Geo_final_updated.json","r") as f:
#     dct=json.load(f)

# data= (json_processing_pipe|update_json_pipe).invoke({
#     "complete_transcript": d,
#     "raw_data":dct,
#     "output_dir":out_path
# })

# with open("data.json",'w') as f:
#     json.dump(data["updated_data"], f, indent=2)


# add_to_pinecone.invoke({
#         "summarized_log":[],
#         "global_context":"",
#         "updated_data":dct
#     })
