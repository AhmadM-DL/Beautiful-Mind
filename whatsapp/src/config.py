from src.utils import load_from_env_or_secret

ORCHESTRATOR_SERVICE_URL = load_from_env_or_secret("ORCHESTRATOR_SERVICE_URL")
META_HANDSHAKE_SECRET = load_from_env_or_secret("META_HANDSHAKE_SECRET")
META_API_KEY = load_from_env_or_secret("META_API_KEY_FILE")
META_WHATSAPP_ID = load_from_env_or_secret("META_WHATSAPP_ID")

