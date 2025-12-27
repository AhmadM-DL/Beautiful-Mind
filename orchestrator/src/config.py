from src.utils import load_from_env_or_secret

AI_SERVICE_URL = load_from_env_or_secret("AI_SERVICE_URL")
BACKEND_SERVICE_URL = load_from_env_or_secret("BACKEND_SERVICE_URL")
