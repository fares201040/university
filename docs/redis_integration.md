# events/redis_integration.md

## Redis Event Publisher and Consumer Integration

This document explains how to use the Redis-based event publisher and consumer classes for event-driven communication in the project.

### RedisEventPublisher
- Publishes events (instances of `Event`) to a specified Redis channel.
- Usage:
  ```python
  from events.redis_publisher import RedisEventPublisher
  from events.models import Event

  publisher = RedisEventPublisher(redis_url="redis://localhost:6379/0")
  event = Event.create(type="BookReserved", payload={"student_id": "123", "book_id": "456"})
  publisher.publish("book.reserved", event)
  ```

### RedisEventConsumer
- Subscribes to a Redis channel and processes incoming events using a handler (subclass of `EventConsumer`).
- Usage:
  ```python
  from events.redis_consumer import RedisEventConsumer, BookReservedHandler

  handler = BookReservedHandler()
  consumer = RedisEventConsumer(redis_url="redis://localhost:6379/0", channel="book.reserved", handler=handler)
  consumer.start()
  ```

### Notes
- The `redis` Python package is required (`pip install redis`).
- All event messages are serialized as JSON.
- Handlers should implement idempotency and error handling for production use.

### Reference
- This integration follows the event-driven and OOP patterns from the book and example codebase.
