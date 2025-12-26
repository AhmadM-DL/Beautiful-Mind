from src.utils import load_from_env_or_secret

OPENAI_API_KEY = load_from_env_or_secret("OPENAI_API_KEY")
OPENAI_CHAT_MODEL = load_from_env_or_secret("OPENAI_CHAT_MODEL")
OPENAI_STT_MODEL = load_from_env_or_secret("OPENAI_STT_MODEL")
