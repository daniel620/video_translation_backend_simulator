import os

# Server settings
MIN_DELAY = int(os.getenv("MIN_DELAY", 10))
MAX_DELAY = int(os.getenv("MAX_DELAY", 30))

# Client settings
INITIAL_INTERVAL = float(os.getenv("INITIAL_INTERVAL", 1.0))
MAX_INTERVAL = float(os.getenv("MAX_INTERVAL", 30.0))
BACKOFF_FACTOR = float(os.getenv("BACKOFF_FACTOR", 1.5))

# Logging level
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")