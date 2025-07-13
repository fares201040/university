import json

import redis

from .base import EventConsumer
from .models import Event


class RedisEventConsumer:
    def __init__(self, redis_url: str, channel: str, handler: EventConsumer):
        self.redis = redis.Redis.from_url(redis_url)
        self.channel = channel
        self.handler = handler

    def start(self):
        pubsub = self.redis.pubsub()
        pubsub.subscribe(self.channel)
        print(f"Subscribed to channel: {self.channel}")
        for message in pubsub.listen():
            if message["type"] == "message":
                data = json.loads(message["data"])
                event = Event(**data)
                self.handler.consume(event)


# Example handler implementation
class BookReservedHandler(EventConsumer):
    def consume(self, event: Event) -> None:
        print(f"Processing event: {event.type} with payload: {event.payload}")


# Example usage:
# handler = BookReservedHandler()
# consumer = RedisEventConsumer(redis_url="redis://localhost:6379/0", channel="book.reserved", handler=handler)
# consumer.start()
