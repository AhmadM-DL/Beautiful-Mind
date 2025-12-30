from src.config import META_API_KEY, WHATSAPP_ID
from src.exceptions import ServiceException
import requests

from logging import getLogger
logger = getLogger(__name__)

VERSION= "v24.0"

class MetaService():
    def __init__(self, api_key, whatsapp_id):
        self.api_key = api_key
        self.whatsapp_id = whatsapp_id
    
    def send_message(self, phone_number, message):
        url = f"https://graph.facebook.com/{VERSION}/{self.whatsapp_id}/messages"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": phone_number,
            "type": "text",
            "text": {
                "preview_url": False,
                "body": message
            }
        }
        try:
            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Failed to send message: {str(e)}")
            raise ServiceException(f"Failed to send message: {str(e)}")

meta_service = MetaService(META_API_KEY, WHATSAPP_ID)