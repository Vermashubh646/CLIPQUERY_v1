import os
from groq import Groq
from app.core.config import settings
# from dotenv import load_dotenv

# load_dotenv('../../../.env')
client = Groq(api_key=settings.GROQ_API_KEY.get_secret_value())
# audio_path='YOUR_AUDIO_PATH'

def transcribe_audio(audio_path):
  with open(audio_path, "rb") as file:
      transcription = client.audio.transcriptions.create(
        file=file,
        model="whisper-large-v3",
        response_format='verbose_json',
        timestamp_granularities=["segment"],
        language="en"
      )
  print('Audio has been transcribed \n',transcription.text[:21],"....")
  return transcription

# def main():
#   out=transcribe_audio(audio_path)
#   print(out.segments[0]['text'])

# if __name__ == "__main__":
#   main()