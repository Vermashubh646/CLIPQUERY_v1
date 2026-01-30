from .video_pipeline.video_clip_extractor import get_video_duration,cut_video_clip
from .video_pipeline.frame_extractor import extract_frame_at_time,frame_to_base64
from .video_pipeline.scene_detect import get_scene_keyframes
from .audio_pipeline.extractor import extract_audio_from_video
from .audio_pipeline.transcriber import transcribe_audio
from .frame_inference.frame_captioning import caption_frames
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
import json
import time

caption_executor = ThreadPoolExecutor(max_workers=5)

# The leading . means:
# from the same package (services)

def caption_frame_from_video(clipped_video_path, time_stamp, output_path_frame,start):

    # clipped video path required as the keyframes are calculated on that basis
    frame = extract_frame_at_time(clipped_video_path,time_stamp,output_path_frame)
    base64_image = frame_to_base64(frame)
    caption = caption_frames(base64_image)

    # free memory explicitly
    del frame
    del base64_image

    print('\n',caption,'\n')

    return {
        'time_stamp':time_stamp+start,
        'captions':caption
    }

def cut_extract_transcript(video_path, output_dir):

    duration = get_video_duration(video_path)
    filename= video_path.split('/')[-1]
    base_name =os.path.splitext(filename)[0]

    if duration is None:
        raise RuntimeError("Video duration could not be determined")

    start=0
    end=45

    print(f"duration is {duration}")

    final_struct=[]

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

            print(f'File clipped successfully at {current_clip_path}')

        keyframes=get_scene_keyframes(current_clip_path)
        if len(keyframes)>3:
            print(f'Sufficient keyframes acquired successfully on the basis of pyscene detection from clip....')
        else:
            keyframes=[]
            for i in range(1,int(end)-start,5):
                keyframes.append(i)
            print(f'Sufficient keyframes acquired successfully on the basis of equal splitting of clip....')

        frames_dir=os.path.splitext(current_clip_path)[0]+'/'
        if not os.path.exists(frames_dir):
            os.mkdir(frames_dir)
        print(f"Storing clip frames at {frames_dir}")

        # Submit captioning tasks for each keyframe.
        # Tasks are queued and executed one-by-one by the executor.
        futures = []
        print("PysceneDetect detected scenes at ",keyframes)
        for time_stamp in keyframes:
            output_path_frame = os.path.join(frames_dir,f"{base_name}_{start+time_stamp}.jpg")
            futures.append(caption_executor.submit(
                caption_frame_from_video,
                current_clip_path,
                time_stamp,
                output_path_frame,
                start
                )
            )

        # Synchronization barrier:
        # Wait until all captioning tasks for this clip are completed.
        visuals_captions=[]
        for future in as_completed(futures):
            visuals_captions.append(future.result())
        print("All captions done for this clip")

        audio_path = os.path.join(output_dir,f"{base_name}_{start}_{end}.mp3")
        extract_audio_from_video(video_path=current_clip_path,output_audio_path=audio_path)

        audio_transcription= transcribe_audio(audio_path)
        audio_segments=[]
        for segment in audio_transcription.segments: # type: ignore
            audio_segments.append({
                "start_time":segment['start']+start,
                "end_time":segment['end']+start,
                "text":segment['text']
            })

        out_struct={
            'start_time':start,
            'end_time':end,
            'audio_transcript':audio_segments,
            'visuals':visuals_captions
        }
        final_struct.append(out_struct)
    
        with open(os.path.join(output_dir,f"{base_name}_final.json"),'w') as f:
                json.dump(final_struct, f, indent=2)
        
        # sliding clip window in the end, so that in between codes can use these
        duration -= 30
        start += 30
        end += 30

        # in order to not to hit api limit
        print("Waiting 20sec to prevent api limit hitting....")
        time.sleep(20)

