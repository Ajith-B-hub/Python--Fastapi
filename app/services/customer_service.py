from __future__ import annotations

import json
from typing import Any

from kafka import KafkaProducer

from app.core.config import settings

producer = KafkaProducer(
    bootstrap_servers=[settings.kafka_bootstrap_servers],
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
    api_version=(2, 8, 0),
)


class KafkaService:
    @staticmethod
    def publish_event(topic: str, event: dict[str, Any]) -> None:
        try:
            producer.send(topic, value=event)
            producer.flush()
        except Exception:
            # Simple, non-blocking failure handling for local/test scenarios
            pass
