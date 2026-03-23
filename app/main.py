from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api.v1.router import api_router
from .core.config import settings
from .core.handlers import register_exception_handlers


app = FastAPI(title="ClipQuery Backend")

# ── CORS ─────────────────────────────────────────────────────
# Allows frontends / external clients on other origins to call
# this API.  Origins are configured via CORS_ALLOWED_ORIGINS
# in .env (defaults to ["*"] for local dev).
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Attach all routes
app.include_router(api_router, prefix="/api")

register_exception_handlers(app)

# input_video = "../Videos/"
# output_path="../Outputs/"
# file_name="Regeneration in Action ｜ Building Resilient Farms in Iowa ｜ National Geographic.mp4"
# base_name =os.path.splitext(file_name)[0]
# out_path=os.path.join(output_path,base_name)
# USER_ID=56985

# data = add_video.invoke({"video_path":os.path.join(input_video,file_name),"output_dir":out_path,"user_id":USER_ID})

# with open("data.json",'w') as f:
#     json.dump(data["processed_json"]["raw_data"], f, indent=2)


