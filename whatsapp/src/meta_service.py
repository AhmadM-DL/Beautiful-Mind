from src.config import META_API_KEY, META_WHATSAPP_ID
from src.exceptions import ServiceException
import requests, base64
from logging import getLogger

logger = getLogger(__name__)

VERSION = "v24.0"

class MetaService:
    def __init__(self, meta_api_key: str, meta_whatsapp_id: str):
        self.meta_api_key = meta_api_key
        self.meta_whatsapp_id = meta_whatsapp_id

    def send_template_message(self, phone_number, template_name, template_language, template_params):
        url = f"https://graph.facebook.com/{VERSION}/{self.meta_whatsapp_id}/messages"
        headers = {
            "Authorization": f"Bearer {self.meta_api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": phone_number,
            "type": "template",
            "template": {
                "name": template_name,
                "language": {
                    "policy": "deterministic",
                    "code": template_language
                },
                "components": [
                    {
                        "type": "body",
                        "parameters": [
                            {
                                "type": "text",
                                "parameter_name": k,
                                "text": v
                            }
                            for k, v in template_params.items()
                        ]
                    }
                ]
            }
        }
        try:
            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Failed to send message: {str(e)}")
            raise ServiceException(f"Failed to send message: {str(e)}")

    def send_thumbs_up(self, phone_number: str, message_id: str):
        url = f"https://graph.facebook.com/{VERSION}/{self.meta_whatsapp_id}/messages"
        payload = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": phone_number,
            "type": "reaction",
            "reaction": {
                "message_id": message_id,
                "emoji": "👍"
            }
        }
        headers = {
            "Authorization": f"Bearer {self.meta_api_key}",
            "Content-Type": "application/json"
        }
        try:
            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Failed to send thumbs up: {str(e)}")
            raise ServiceException(f"Failed to send thumbs up: {str(e)}")

    def get_media_as_base64(self, media_url: str):
        headers = {
            "Authorization": f"Bearer {self.meta_api_key}",
            "Content-Type": "application/json"
        }
        try:
            response = requests.get(media_url, headers=headers)
            response.raise_for_status()
            encoded = base64.b64encode(response.content).decode('utf-8')
            return encoded
        except Exception as e:
            logger.error(f"Failed to get media: {str(e)}")
            raise ServiceException(f"Failed to get media: {str(e)}")

meta_service = MetaService(META_API_KEY, META_WHATSAPP_ID)
