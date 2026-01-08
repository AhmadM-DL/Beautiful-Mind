from src.config import WHATSAPP_SERVICE_URL, META_HANDSHAKE_SECRET, APP_DOMAIN
from src.exceptions import ServiceException
import requests

from logging import getLogger
logger = getLogger(__name__)

class MetaService():
    def __init__(self, whatsapp_service_url, handshake_secret, app_domain):
        self.whatsapp_service_url = whatsapp_service_url
        self.handshake_secret = handshake_secret
        self.app_domain = app_domain
    
    def greet_patient(self, phone_number, password):
        url = f"{self.whatsapp_service_url}/greet_patient"
        headers = {
            "Authorization": f"Bearer {self.handshake_secret}",
            "Content-Type": "application/json"
        }
        data = {
            "phone_number": phone_number,
            "url": self.app_domain,
            "password": password,
        }
        try:
            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Failed to greet patient: {str(e)}")
            raise ServiceException(f"Failed to greet patient: {str(e)}")

meta_service = MetaService(WHATSAPP_SERVICE_URL, META_HANDSHAKE_SECRET, APP_DOMAIN)