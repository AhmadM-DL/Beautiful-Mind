from src.config import ORCHESTRATOR_SERVICE_URL
import requests
from src.exceptions import ServiceException

from logging import getLogger
logger = getLogger(__name__)
 
class OrchestratorService:
    def __init__(self, orchestrator_service_url: str):
        self.base_url = orchestrator_service_url
    
    def process_voice_note(self, phone_number: str, base64_audio: str):
        url = f"{self.base_url}/process_voice_note"
        payload = {
            "phone_number": phone_number,
            "base64_audio": base64_audio
        }
        try:
            response = requests.post(url, json=payload)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Failed to process voice note: {str(e)}")
            raise ServiceException(f"Failed to process voice note: {str(e)}")

orchestrator_service = OrchestratorService(ORCHESTRATOR_SERVICE_URL)
