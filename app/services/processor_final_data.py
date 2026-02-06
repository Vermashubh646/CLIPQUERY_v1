from .global_context.global_context_extractor import global_context_pipe
from .json_serialize.json_serialize import get_logs_runnable
from .processor_raw import cut_extract_transcript
from .summarizer_model.llm_summarizer import summarizer_pipe
from .integrate_s3_bucket.bucket import upload_to_bucket

from langchain_core.runnables import RunnableLambda, RunnableParallel
from concurrent.futures import ThreadPoolExecutor, as_completed
import os
import json

# pipeline function for raw data extraction
raw_pipe = RunnableLambda(lambda x: cut_extract_transcript(video_path=x["video_path"],output_dir=x['output_dir']))# type: ignore

# parallel chain for extracting global context
parallel_global_context=RunnableParallel({
    "global_context": RunnableLambda(lambda x: x['complete_transcript']) | global_context_pipe,
    "raw_data" : RunnableLambda(lambda x: x['raw_data']), 
    "output_dir" : RunnableLambda(lambda x: x['output_dir']) 
})

def parallel_summarize_clips(parallel_global_context_output):

    raw_data=parallel_global_context_output["raw_data"]
    global_context = parallel_global_context_output["global_context"]
    max_workers=4

    # creating summarize func for a clip
    def summarize_one(clip):
        return summarizer_pipe.invoke({
            "global_context": global_context,
            **get_logs_runnable.invoke(clip)
        })

    results = [None] * len(raw_data)

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {
            executor.submit(summarize_one, clip): i
            for i, clip in enumerate(raw_data)
        }

        for future in as_completed(futures):
            idx = futures[future]
            results[idx] = future.result()

    return  {
        "summarized_log":results,
        ** parallel_global_context_output
        }


# parallel chain to extract summarized_log
parallel_summarize_json=RunnableLambda(parallel_summarize_clips)

json_processing_pipe =(
    parallel_global_context | parallel_summarize_json
)

def update_json(updated_video_data):

    processed_json = updated_video_data['processed_json']
    bucket_data = updated_video_data['bucket_data']
    
    for clip,summary in zip(processed_json["raw_data"],processed_json["summarized_log"]):
        clip['clip_narrative'] = summary
        clip["video_id"]= bucket_data["video_id"]        
        clip["bucket"]= bucket_data["bucket"]           
        clip["key"]=bucket_data["key"] 
    
    # writing new json
    base_name=processed_json["output_dir"].split("/")[-1]
    file_path=os.path.join(processed_json["output_dir"],f"{base_name}_final_updated.json")
    with open(file_path,'w') as f:
        json.dump(processed_json["raw_data"], f, indent=2)
                
    print(f"New updated json at {file_path}")

    return updated_video_data

# pipeline function for raw data extraction
update_json_pipe = RunnableLambda(update_json)

# parallelize the video processing and bucket storing pipe
parallel_combined_pipe=RunnableParallel({
    "processed_json":raw_pipe | json_processing_pipe,
    "bucket_data": upload_to_bucket,
})

# final combined pipeline
ultimate_video_pipe=(
    parallel_combined_pipe | update_json_pipe
)



