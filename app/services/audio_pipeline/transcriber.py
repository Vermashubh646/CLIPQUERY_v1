from groq import Groq

from app.core.config import settings
from app.core.logger import custom_logger

client = Groq(api_key=settings.GROQ_API_KEY.get_secret_value())

def transcribe_audio(audio_path):
  with open(audio_path, "rb") as file:
      transcription = client.audio.transcriptions.create(
        file=file,
        model="whisper-large-v3",
        response_format='verbose_json',
        timestamp_granularities=["segment"],
        language="en"
      )
  custom_logger.info('Audio has been transcribed \n',transcription.text[:21],"....")
  return transcription
