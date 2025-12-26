from fastapi import FastAPI, UploadFile, File, HTTPException
from src.stt import stt_service
from src.anonymizer import anonymizer_service
from src.schema import AnonymizeRequest, STTRequest
from logging import getLogger
logger = getLogger(__name__)

app = FastAPI(title="BeautifulMind AI Service")

@app.post("/api/stt")
async def speech_to_text(request: STTRequest):
    try:
        transcription = stt_service.transcribe(request.base64_audio)
        return {"transcription": transcription}
    except Exception as e:
        logger.error("Failed to transcribe audio: %s", e)
        raise HTTPException(status_code=500)

@app.post("/api/anonymize")
async def anonymize_text(request: AnonymizeRequest):
    try:
        anonymized = anonymizer_service.anonymize(request.text)
        return {"anonymized_text": anonymized}
    except Exception as e:
        logger.error("Failed to anonymize text: %s", e)
        raise HTTPException(status_code=500)
