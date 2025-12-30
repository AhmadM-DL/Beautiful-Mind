from src.utils import load_from_env_or_secret

AI_SERVICE_URL = load_from_env_or_secret("AI_SERVICE_URL")
BACKEND_SERVICE_URL = load_from_env_or_secret("BACKEND_SERVICE_URL")
META_API_KEY = load_from_env_or_secret("META_API_KEY_FILE")
WHATSAPP_ID = load_from_env_or_secret("WHATSAPP_ID")
