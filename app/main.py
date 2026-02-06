import os
import json
from dotenv import load_dotenv

load_dotenv('.env')

from fastapi import FastAPI
from .api.v1.router import api_router

app = FastAPI(title="ClipQuery Backend")

# Attach all routes
app.include_router(api_router, prefix="/api")


# input_video = "../Videos/"
# output_path="../Outputs/"
# file_name="Regeneration in Action ｜ Building Resilient Farms in Iowa ｜ National Geographic.mp4"
# base_name =os.path.splitext(file_name)[0]
# out_path=os.path.join(output_path,base_name)
# USER_ID=56985

# data = add_video.invoke({"video_path":os.path.join(input_video,file_name),"output_dir":out_path,"user_id":USER_ID})

# with open("data.json",'w') as f:
#     json.dump(data["processed_json"]["raw_data"], f, indent=2)


