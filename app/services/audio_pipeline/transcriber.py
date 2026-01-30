import os
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv('../../../.env')

client = Groq()

filename = "../../../Outputs/The Snowflake Myth.mp3"

with open(filename, "rb") as file:
    transcription = client.audio.transcriptions.create(
      file=file,
      model="whisper-large-v3",
      prompt="Make sure the segments are divide contexually.",
      response_format="verbose_json",  # Optional
      timestamp_granularities = ["segment"], 
      language="en"
    )
print(json.dumps(transcription, indent=4, default=str))

