import json

import redis

from .models import Event


class RedisEventPublisher:
    def __init__(self, redis_url: str):
        self.redis = redis.Redis.from_url(redis_url)

    def publish(self, channel: str, event: Event) -> None:
        message = event.json()
        self.redis.publish(channel, message)


# Example usage:
# publisher = RedisEventPublisher(redis_url="redis://localhost:6379/0")
# event = Event.create(type="BookReserved", payload={"student_id": "123", "book_id": "456"})
# publisher.publish("book.reserved", event)
