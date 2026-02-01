from langchain_core.runnables import RunnableLambda

def get_audio_video_data(clip_dict):

    audio_log=""
    for item in clip_dict["audio_transcript"]:
        audio_log+=f"[{item.get("start_time",None):.2f}s - {item.get("end_time",None):.2f}s] {item["text"]} \n"
    
    video_log=""
    for item in clip_dict["visuals"]:
        video_log+=f"[ {item.get("time_stamp",None):.2f}s ] {item["captions"]} \n"
    
    return {
        "audio_log":audio_log,
        "visual_log":video_log
        }


get_logs_runnable = RunnableLambda(get_audio_video_data)
