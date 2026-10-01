from __future__ import annotations

import json
from typing import Any

import redis

from app.core.config import settings

redis_client = redis.Redis.from_url(settings.redis_url, decode_responses=True)


class RedisService:
    @staticmethod
    def set_value(key: str, value: Any, ttl: int | None = None) -> None:
        payload = json.dumps(value)
        if ttl is not None:
            redis_client.setex(key, ttl, payload)
        else:
            redis_client.set(key, payload)

    @staticmethod
    def get_value(key: str) -> Any | None:
        value = redis_client.get(key)
        if value is None:
            return None
        return json.loads(value)

    @staticmethod
    def delete_value(key: str) -> None:
        redis_client.delete(key)

    @staticmethod
    def ping() -> bool:
        try:
            return bool(redis_client.ping())
        except Exception:
            return False
