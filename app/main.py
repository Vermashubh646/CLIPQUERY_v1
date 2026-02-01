import os
from dotenv import load_dotenv

load_dotenv('.env')

from services.processor import cut_extract_transcript

input_video = "../Videos/"
output_audio_path="../Outputs/"
file_name="Improving Mindsets & Lives During Health Challenges ｜ Limitless： Live Better Now ｜ Nat Geo.mkv"
base_name =os.path.splitext(file_name)[0]
out_path=os.path.join(output_audio_path,base_name)

if not os.path.exists(out_path):
    os.mkdir(out_path)
cut_extract_transcript(video_path=os.path.join(input_video,file_name),output_dir=out_path)