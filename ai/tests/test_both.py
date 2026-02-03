import base64
from src.anonymizer import anonymizer_service
from src.stt import stt_service

from logging import getLogger

logger = getLogger(__name__)

def test_both():
    with open("./tests/test_audio_real.mp3", "rb") as f:
        base64_audio = base64.b64encode(f.read()).decode("utf-8")
        transcription = stt_service.transcribe(base64_audio)
        anonymized_text = anonymizer_service.anonymize(transcription)
        logger.info(f"Transcription: {transcription}")
        logger.info(f"Anonymized Text: {anonymized_text}")