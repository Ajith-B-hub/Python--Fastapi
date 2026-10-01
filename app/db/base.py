from __future__ import annotations

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

from app.core.config import settings

logger = logging.getLogger("customer_api")
logger.setLevel(logging.INFO)
logger.propagate = False

logs_dir = Path("logs")
logs_dir.mkdir(exist_ok=True)

file_handler = RotatingFileHandler(logs_dir / "app.log", maxBytes=5 * 1024 * 1024, backupCount=5)
file_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(name)s - %(message)s"))
logger.addHandler(file_handler)

console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
logger.addHandler(console_handler)

if settings.debug:
    logger.setLevel(logging.DEBUG)
