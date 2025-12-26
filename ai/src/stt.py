import os   
from openai import OpenAI
from src.config import OPENAI_API_KEY, OPENAI_STT_MODEL
from src.exceptions import ServiceException
import base64
import tempfile

from logging import getLogger
logger = getLogger(__name__)
    
class STTService:
    def __init__(self):
        try: 
            self.client = OpenAI(api_key=OPENAI_API_KEY)
        except Exception as e:
            logger.error("Failed to initialize OpenAI client: %s", e)
            raise ServiceException("Failed to initialize OpenAI client")

    def transcribe(self, base64_audio: str) -> str:
        try:
            audio_file = base64.b64decode(base64_audio)
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_file:
                temp_file.write(audio_file)
                audio_file_path = temp_file.name
            with open(audio_file_path, "rb") as audio_file:
                transcript = self.client.audio.transcriptions.create(
                    model=OPENAI_STT_MODEL, 
                    file=audio_file,
                    language="ar"
                )
        except Exception as e:
            logger.error("Failed to transcribe audio: %s", e)
            raise ServiceException("Failed to transcribe audio")
        finally:
            if os.path.exists(audio_file_path):
                os.remove(audio_file_path)
        return transcript.text

stt_service = STTService()
