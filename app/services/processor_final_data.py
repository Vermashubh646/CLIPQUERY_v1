from .global_context.global_context_extractor import global_context_pipe
from .json_serialize.json_serialize import get_logs_runnable
from .processor_raw import cut_extract_transcript
from .summarizer_model.llm_summarizer import summarizer_pipe

from langchain_core.runnables import RunnableLambda, RunnableParallel
from typing import TypedDict


# pipeline function for raw data extraction
raw_pipe = RunnableLambda(lambda x: cut_extract_transcript(video_path=x["video_path"],output_dir=x['output_dir']))# type: ignore

parallel_global_context=RunnableParallel({
    "global_context": RunnableLambda(lambda x: x['complete_transcript']) | global_context_pipe,
    "raw_data" : RunnableLambda(lambda x: x['raw_data']) 
})


json_processing_pipe =(
    parallel_global_context |
    RunnableLambda(
        lambda x: [
            summarizer_pipe.invoke({
                "global_context":x['global_context'], # type: ignore
                **get_logs_runnable.invoke(clip_data)
            })
            for clip_data in x["raw_data"] # type: ignore
        ]   
    )
)

ultimate_video_pipe=(
    raw_pipe | json_processing_pipe
)



