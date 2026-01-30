from .video_pipeline.video_clip_extractor import get_video_duration,cut_video_clip
from .video_pipeline.frame_extractor import extract_frame_at_time
from .video_pipeline.scene_detect import get_scene_keyframes
from .audio_pipeline.extractor import extract_audio_from_video
import os

# The leading . means:
# from the same package (services)

def cut_extract_transcript(video_path, output_dir):

    duration = get_video_duration(video_path)
    filename= video_path.split('/')[-1]
    base_name =os.path.splitext(filename)[0]

    if duration is None:
        raise RuntimeError("Video duration could not be determined")

    start=0
    end=45

    print(f"duration is {duration}")
    continue_loop = True

    while duration>0 and continue_loop:

        if duration<=2*(end-start-15):
            continue_loop=False
            end= start + duration
            if start != 0:
                current_clip_path=os.path.join(output_dir,f"{base_name}_{start}_{end}.mp4")
                cut_video_clip(video_path,start_time=start,end_time=end,output_path=current_clip_path)
        
                print(f'File clipped successfully at {current_clip_path}')
            else:
                current_clip_path = video_path        
        else:

            current_clip_path=os.path.join(output_dir,f"{base_name}_{start}_{end}.mp4")
            cut_video_clip(video_path,start_time=start,end_time=end,output_path=current_clip_path)

            duration -= 30
            start += 30
            end += 30

            print(f'File clipped successfully at {current_clip_path}')

        keyframes=get_scene_keyframes(current_clip_path)
        print(f'Keyframes acquired successfully....')

        frames_dir=os.path.splitext(current_clip_path)[0]+'/'
        if not os.path.exists(frames_dir):
            os.mkdir(frames_dir)

        print(f"Storing clip frames at {frames_dir}")
        for time_stamp in keyframes:
            output_path_frame = os.path.join(frames_dir,f"{base_name}_{time_stamp}.jpg")
            extract_frame_at_time(video_path,time_stamp,output_path_frame)
        
        audio_path = os.path.join(output_dir,f"{base_name}.mp3")
        extract_audio_from_video(video_path=video_path,output_audio_path=audio_path)

