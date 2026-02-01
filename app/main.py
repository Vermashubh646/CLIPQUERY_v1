import os
import json
from dotenv import load_dotenv

load_dotenv('.env')

from services.processor_final_data import ultimate_video_pipe,json_processing_pipe

input_video = "../Videos/"
output_audio_path="../Outputs/"
file_name="Improving Mindsets & Lives During Health Challenges ｜ Limitless： Live Better Now ｜ Nat Geo.mkv"
base_name =os.path.splitext(file_name)[0]
out_path=os.path.join(output_audio_path,base_name)


data=ultimate_video_pipe.invoke({"video_path":os.path.join(input_video,file_name),"output_dir":out_path})

# with open("/home/kamadahanam/Documents/ALL_WORKS/CLIPQUERY_UPGRADED/Outputs/Improving Mindsets & Lives During Health Challenges ｜ Limitless： Live Better Now ｜ Nat Geo/Improving Mindsets & Lives During Health Challenges ｜ Limitless： Live Better Now ｜ Nat Geo_complete_transcript.txt","r") as f:
#     d = f.read()

# with open("/home/kamadahanam/Documents/ALL_WORKS/CLIPQUERY_UPGRADED/Outputs/Improving Mindsets & Lives During Health Challenges ｜ Limitless： Live Better Now ｜ Nat Geo/Improving Mindsets & Lives During Health Challenges ｜ Limitless： Live Better Now ｜ Nat Geo_final.json","r") as f:
#     dct=json.load(f)

# data= json_processing_pipe.invoke({
#     "complete_transcript": d,
#     "raw_data":dct
# })

str_data= ""
for i in data:
    str_data+=f"{i}\n\n"

with open("data.txt","w") as f:
    f.write(str_data)# type: ignore