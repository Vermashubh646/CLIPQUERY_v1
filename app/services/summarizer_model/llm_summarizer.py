from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel, RunnableLambda
import os

# from dotenv import load_dotenv
# load_dotenv('../../../.env')

model = ChatGroq(model="llama-3.3-70b-versatile")

prompt_summarizer = PromptTemplate(
    template="""
        You are a Universal Forensic Video Analyst. Your task is to reconstruct a video segment into a dense, searchable text record.


        OBJECTIVE:
        Fuse the audio and visual logs into a single, seamless narrative that preserves 100% of the searchable entities. The output must allow a search engine to find this clip based on ANY specific detail shown or spoken.

        UNIVERSAL GUIDELINES (Apply strict adherence):

        1. **ENTITY HYPER-SPECIFICITY**
        - **Never** summarize as "The user typed a command" or "The speaker showed a chart."
        - **Always** explicitly state the content: "The user typed 'sudo apt update'" or "The speaker displayed a pie chart showing 45% Growth."
        - Capture ALL proper nouns, error codes, book titles, software names, and scientific terms.

        2. **VISUAL TEXT EXTRACTION (OCR)**
        - If the Visual Log mentions on-screen text (slides, subtitles, code, handwritten notes), you MUST transcribe it verbatim into the narrative.
        - For fast-paced/flashy videos: Ignore decorative transitions, but prioritize data-rich overlays (pop-up facts, citations, diagrams).

        3. **MULTIMODAL DISAMBIGUATION**
        - **Fix Pronouns:** If Audio says "Look at *this*," use the Visual timestamp to replace "*this*" with the specific object (e.g., "Look at the [Redacted Document]").
        - **Fix Context:** If Audio is metaphorical (e.g., "It's a monster"), use Visuals to ground it (e.g., "Referring to the massive Category 5 hurricane on the satellite map").

        4. **NARRATIVE FLOW & ATTRIBUTION**
        - For Movies/Drama: Attribute dialogue to the visible character actions (e.g., "John draws his weapon while shouting...").
        - For Tutorials/Science: Link the explanation to the demonstration (e.g., "As Dr. Smith explains friction, the animation shows two rough surfaces interlocking").

        5. **TIMESTAMP SYNCHRONIZATION**
        - Use the timestamps in the logs to ensure the narrative is chronologically correct. Do not mix up the order of events.

        OUTPUT FORMAT:
        Return ONLY the raw narrative text.Allowed to be long and detailed.If Multiple paragraphs are needed, just make then one long string. Do not include markdown, preambles, or "Here is the summary."

        GLOBAL CONTEXT: "{global_context}"

        INPUT DATA:
        - AUDIO LOG: 
        {audio_log}.\n
        - VISUAL LOG: 
        {visual_log}.
    """,
    input_variables=['global_context','audio_log','visual_log']
)

parser = StrOutputParser()

def print_out(text):
    print(text)
    return text

print_output=RunnableLambda(print_out)

summarizer_pipe = prompt_summarizer | model | parser |print_output


# print(summarize_pipe.invoke({
# 'global_context':"",
# 'audio_log':"",
# 'visual_log':""
# }))
