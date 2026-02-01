from .global_context.global_context_extractor import global_context_pipe
from .json_serialize.json_serialize import get_logs_runnable
from .processor_raw import cut_extract_transcript
from .summarizer_model.llm_summarizer import summarizer_pipe

from langchain_core.runnables import RunnableLambda, RunnableParallel
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

# parallel chain to extract summarized_log
parallel_process_json=RunnableParallel({
    "summarized_log":RunnableLambda(
        lambda x: [
            summarizer_pipe.invoke({
                "global_context":x['global_context'], # type: ignore
                **get_logs_runnable.invoke(clip_data)
            })
            for clip_data in x["raw_data"] # type: ignore
        ]   
    ),
    "global_context": RunnableLambda(lambda x: x['global_context']),
    "raw_data" : RunnableLambda(lambda x: x['raw_data']), 
    "output_dir" : RunnableLambda(lambda x: x['output_dir'])  
})

json_processing_pipe =(
    parallel_global_context | parallel_process_json
)

def update_json(summarized_log,global_context,raw_data,output_dir):
    for clip,summary in zip(raw_data,summarized_log):
        clip['clip_narrative'] = summary
    
    # writing new json
    base_name=output_dir.split("/")[-1]
    file_path=os.path.join(output_dir,f"{base_name}_final_updated.json")
    with open(file_path,'w') as f:
                json.dump(raw_data, f, indent=2)
                
    print(f"New updated json at {file_path}")

    return {
        "summarized_log":summarized_log,
        "global_context":global_context,
        "updated_data":raw_data
    }

# pipeline function for raw data extraction
update_json_pipe = RunnableLambda(lambda x: update_json(
       summarized_log=x["summarized_log"],global_context=x['global_context'],raw_data=x['raw_data'],output_dir=x['output_dir']))# type: ignore


# final combined pipeline
ultimate_video_pipe=(
    raw_pipe | json_processing_pipe | update_json_pipe
)



