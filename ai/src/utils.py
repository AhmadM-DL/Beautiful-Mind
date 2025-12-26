import os

def load_from_env_or_secret(key):
    value = os.getenv(key)
    if os.path.exists(value):
        with open(value, 'r') as f:
            return f.read().strip()
    else:
        return value    