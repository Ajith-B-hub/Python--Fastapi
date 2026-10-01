from __future__ import annotations

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# Define friendly defaults for local development
APP_ENV = "development"
PROJECT_NAME = "FastAPI Enterprise Customer API"
VERSION = "1.0.0"

# File paths
DB_PATH = BASE_DIR / "data" / "app.db"
LOGS_DIR = BASE_DIR / "logs"

# Resource settings
DEFAULT_USERNAME = "admin"
DEFAULT_PASSWORD = "admin123"
JWT_SECRET_KEY = "CHANGE_ME_IN_ENV"
JWT_ALGORITHM = "HS256"
JWT_EXPIRE_MINUTES = 60

REDIS_HOST = "localhost"
REDIS_PORT = 6379
REDIS_DB = 0
REDIS_URL = f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}"

KAFKA_BOOTSTRAP_SERVERS = "localhost:9092"
KAFKA_TOPIC = "customer-events"

# Application config
DEBUG = True
