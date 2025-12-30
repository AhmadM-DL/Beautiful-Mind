from src.config import AI_SERVICE_URL, BACKEND_SERVICE_URL
import requests
from src.exceptions import ServiceException
from fastapi import HTTPException
import logging

logger = logging.getLogger(__name__)

class OrchestrationService():

    def login_by_phone(self, phone_number: str):
        logger.info("Login attempt...")
        try:
            login_resp = requests.post(
                f"{BACKEND_SERVICE_URL}/api/patient/login-by-phone-number",
                json={
                    "phone_number": phone_number,
                }
            )
            login_resp.raise_for_status()
            token = login_resp.json().get("token")
            return token
        except Exception as e:
            logger.error(f"Backend Login Error: {e}")
            raise ServiceException(f"Backend Login Error: {e}")
            
    def process_voice_note(self, token: str, base64_audio: str):
        # 1. Transcription (STT)
        logger.info("Transcribing audio...")
        try:
            stt_resp = requests.post(
                f"{AI_SERVICE_URL}/api/stt",
                json={"base64_audio": base64_audio},
            )
            stt_resp.raise_for_status()
            transcription = stt_resp.json().get("transcription")
        except Exception as e:
            logger.error(f"STT Error: {e}")
            raise ServiceException(f"STT Error: {e}")

        # 2. Anonymization
        logger.info("Anonymizing transcription...")
        try:
            anon_resp = requests.post(
                f"{AI_SERVICE_URL}/api/anonymize",
                json={"text": transcription},
                timeout=None
            )
            anon_resp.raise_for_status()
            anonymized_text = anon_resp.json().get("anonymized_text")
        except Exception as e:
            logger.error(f"Anonymization Error: {e}")
            raise ServiceException(f"Anonymization Error: {e}")

        # 3. Create Note
        logger.info("Creating note in backend...")
        try:
            note_resp = requests.post(
                f"{BACKEND_SERVICE_URL}/api/patient/add-note",
                json={"note": anonymized_text},
                headers={"Authorization": f"Bearer {token}"}
            )
            note_resp.raise_for_status()
            return {"status": "success"}
        except Exception as e:
            logger.error(f"Create Note Error: {e}")
            raise ServiceException(f"Create Note Error: {e}")

orchestration_service = OrchestrationService()