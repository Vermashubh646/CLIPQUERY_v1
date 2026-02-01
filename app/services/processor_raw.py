from .video_pipeline.video_clip_extractor import get_video_duration,cut_video_clip
from .video_pipeline.frame_extractor import extract_frame_at_time,frame_to_base64
from .video_pipeline.scene_detect import get_scene_keyframes
from .audio_pipeline.extractor import extract_audio_from_video
from .audio_pipeline.transcriber import transcribe_audio
from .frame_inference.frame_captioning import caption_frames
from concurrent.futures import ThreadPoolExecutor, as_completed
import json
import time
import os

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


def process_clip(needs_cut,video_path,current_clip_path,frames_dir,audio_path,start,end,base_name):

    # clip video if needed
    if needs_cut:
        cut_video_clip(video_path,start_time=start,end_time=end,output_path=current_clip_path)
        print(f'File clipped successfully at {current_clip_path}')

    # extract keyframes
    keyframes=get_scene_keyframes(current_clip_path)

    if len(keyframes)>3:
        print(f'Sufficient keyframes acquired successfully on the basis of pyscene detection from clip....')
    else:
        keyframes=[]
        for i in range(1,int(end)-start,5):
            keyframes.append(i)
        print(f'Extra keyframes acquired successfully on the basis of equal splitting of clip....')
    
    print("PysceneDetect detected scenes at ",keyframes)

    
    # Submit captioning tasks for each keyframe.
    # Tasks are queued and executed one-by-one by the executor.
    futures = []
    for time_stamp in keyframes:

        # defining path for frame
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


    #extract audio file from clip 
    extract_audio_from_video(video_path=current_clip_path,output_audio_path=audio_path)


    # transcript audio and store in segements
    audio_transcription= transcribe_audio(audio_path)
    audio_segments=[]
    for segment in audio_transcription.segments: # type: ignore
        audio_segments.append({
            "start_time":segment['start']+start,
            "end_time":segment['end']+start,
            "text":segment['text']
        })

    return visuals_captions, audio_segments, audio_transcription.text



def cut_extract_transcript(video_path, output_dir):

    if not os.path.exists(output_dir):
        os.mkdir(output_dir)

    duration = get_video_duration(video_path)
    base_name =os.path.splitext(video_path.split('/')[-1])[0]

    if duration is None:
        raise RuntimeError("Video duration could not be determined")

    start=0
    end=45

    WINDOW = 45
    STRIDE = 30
    TAIL_BUFFER = 15 

    print(f"duration is {duration}")

    final_struct=[]
    complete_transcript=""

    while duration>0 :
        
        isFinalClip = duration < 2*(WINDOW - TAIL_BUFFER)

        if isFinalClip:
            end = start+duration 

        needs_cut = not (start ==0 and isFinalClip)

        if needs_cut:
            current_clip_path=os.path.join(output_dir,f"{base_name}_{start}_{end}.mp4")
            
        else:
            current_clip_path = video_path 
            print(f'Usint original video completely at {current_clip_path}')

        # creating frames directory
        frames_dir=os.path.splitext(current_clip_path)[0]+'/'
        if not os.path.exists(frames_dir):
            os.mkdir(frames_dir)
        print(f"Storing clip frames at {frames_dir}")

        # definig path of audio file
        audio_path = os.path.join(output_dir,f"{base_name}_{start}_{end}.mp3")

        visuals_captions, audio_segments, full_transcipt= process_clip(needs_cut,video_path,current_clip_path,frames_dir,audio_path,start,end,base_name)

        complete_transcript+=full_transcipt

        out_struct={
            'start_time':start,
            'end_time':end,
            'audio_transcript':audio_segments,
            'visuals':visuals_captions
        }
        final_struct.append(out_struct)
    
        # for reference purpose
        with open(os.path.join(output_dir,f"{base_name}_final.json"),'w') as f:
                json.dump(final_struct, f, indent=2)
        
        # for reference purpose
        with open(os.path.join(output_dir,f"{base_name}_complete_transcript.txt"),'w') as f:
                f.write(complete_transcript)
        
        # sliding clip window in the end, so that in between codes can use these
        duration -= STRIDE
        start += STRIDE
        end += STRIDE

        if isFinalClip:
            break

        # in order to not to hit api limit
        print("Waiting 30sec to prevent api limit hitting....")
        time.sleep(30)
    print("Raw data extraction process over....")

    return {
        "raw_data":final_struct, "complete_transcript":complete_transcript
    }

