import hashlib
import json
from openai import OpenAI
from src.config import OPENAI_API_KEY, OPENAI_CHAT_MODEL
from src.exceptions import ServiceException

from logging import getLogger
logger = getLogger(__name__)

class AnonymizerService:
    def __init__(self):
        try:
            self.client = OpenAI(api_key=OPENAI_API_KEY)
        except Exception as e:
            logger.error("Failed to initialize OpenAI client: %s", e)
            raise ServiceException(f"Failed to initialize OpenAI client: {e}")
        self.model = OPENAI_CHAT_MODEL

    def anonymize(self, text: str) -> str:
        prompt = (
            "You are a helpful assistant that identifies names of people and places in text for anonymization. "
            "Identify all names of people and places in the text provided below. "
            "Return the result ONLY as a JSON object with a key 'entities' containing a list of objects, "
            "each containing 'text' (the original name) and 'type' for types person and place use the language of the text"
            "For example if the text is in Arabic return the type in Arabic"
            'If no entities are found, return {"entities": []}.\n\n'
            f"Text: {text}"
        )

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
            )
        except Exception as e:
            logger.error("Failed to get response from OpenAI: %s", e)
            raise ServiceException(f"Failed to get response from OpenAI: {e}")

        content = response.choices[0].message.content
        try:
            data = json.loads(content)
            entities = data.get("entities") 
        except Exception as e:
            logger.error("Failed to parse response %s from OpenAI: %s", content, e)
            raise ServiceException(f"Failed to parse response from OpenAI: {e}")

        anonymized_text = text
        for entity in entities:
            original = entity["text"]
            entity_type = entity["type"]
            hashed = hashlib.sha256(original.encode()).hexdigest()[:6]
            replacement = f"{entity_type} {hashed}"
            anonymized_text = anonymized_text.replace(original, replacement)

        return anonymized_text

anonymizer_service = AnonymizerService()