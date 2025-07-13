from abc import ABC, abstractmethod
from typing import Any, Dict

from .models import Event


class EventProducer(ABC):
    @abstractmethod
    def publish(self, event: Event) -> None:
        """Publish an event to the broker."""
        pass


class EventConsumer(ABC):
    @abstractmethod
    def consume(self, event: Event) -> None:
        """Consume an event from the broker."""
        pass


class EventHandlerFactory:
    """Factory for registering and retrieving event handlers by event type."""

    def __init__(self):
        self._handlers: Dict[str, EventConsumer] = {}

    def register_handler(self, event_type: str, handler: EventConsumer):
        self._handlers[event_type] = handler

    def get_handler(self, event_type: str) -> EventConsumer:
        return self._handlers.get(event_type)
