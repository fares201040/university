from datetime import datetime
from typing import Any, Dict

from pydantic import BaseModel


class Event(BaseModel):
    type: str
    version: str
    timestamp: str
    payload: Dict[str, Any]
    metadata: Dict[str, Any] = {}

    @classmethod
    def create(
        cls,
        type: str,
        payload: Dict[str, Any],
        version: str = "1.0",
        metadata: Dict[str, Any] = None,
    ) -> "Event":
        return cls(
            type=type,
            version=version,
            timestamp=datetime.utcnow().isoformat() + "Z",
            payload=payload,
            metadata=metadata or {},
        )


# Example of extending the base Event for a specific use case
class BookReservedEvent(Event):
    type: str = "BookReserved"
    # Optionally, add more specific fields or methods here
