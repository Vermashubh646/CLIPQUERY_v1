from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
import os

# from dotenv import load_dotenv
# load_dotenv('../../../.env')

model = ChatGroq(
    model="llama-3.3-70b-versatile")

prompt_global_context = PromptTemplate(
    template="""
    You are a context extractor.
    You will be provided with an audio transcript of a video, for which global context is to be extracted.
    Summarize the main topic, specific technical terminology, and speaker intent from this transcript in 2 sentences.
    It should not be more than 45 words.
    transcript:{transcript}
    """,
    input_variables=['transcript']
)

parser = StrOutputParser()

global_context_pipe = prompt_global_context | model | parser


# insider=input("What is the transcript?\n")
# print('\n\n',global_context_pipe.invoke({"transcript":insider}))
