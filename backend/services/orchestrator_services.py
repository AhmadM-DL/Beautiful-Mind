from django.conf import settings
from services.exceptions import ServiceException
import requests

from logging import getLogger
logger = getLogger(__name__)

class OrchestratorService():
    def __init__(self, orchestrator_service_url):
        self.orchestrator_service_url = orchestrator_service_url

    def greet_patient(self, phone_number, password):
        url = f"{self.orchestrator_service_url}/greet_patient"
        payload = {
            "phone_number": phone_number,
            "password": password,
        }
        try:
            response = requests.post(url, json=payload)
            response.raise_for_status()
        except Exception as e:
            logger.error(f"Failed to greet patient: {str(e)}")
            raise ServiceException(f"Failed to greet patient: {str(e)}")
        return response.json()

orchestrator_service = OrchestratorService(settings.ORCHESTRATOR_SERVICE_URL)