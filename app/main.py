import os
from dotenv import load_dotenv

load_dotenv('.env')

from services.processor import cut_extract_transcript

input_video = "../Videos/"
output_audio_path="../Outputs/"
file_name="The Snowflake Myth.mp4"
base_name =os.path.splitext(file_name)[0]

cut_extract_transcript(video_path=os.path.join(input_video,file_name),output_dir=output_audio_path)