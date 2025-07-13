# Shared Event Models & OOP Patterns

This document describes the shared event models and object-oriented programming patterns used for event-driven communication.

## Shared Event Models
- Define a base `Event` class with fields: `type`, `version`, `timestamp`, `payload`, `metadata`.
- Use Pydantic or dataclasses for validation and serialization.
- All event types inherit from the base `Event` class.

## OOP Patterns
- Abstract base classes for event producers and consumers.
- Dependency injection for broker clients and configuration.
- Factory pattern for event handler registration.

## Example
```python
from pydantic import BaseModel
from typing import Dict, Any

class Event(BaseModel):
    type: str
    version: str
    timestamp: str
    payload: Dict[str, Any]
    metadata: Dict[str, Any] = {}
```

## Extensibility
- Add new event types by subclassing the base `Event` class.
- Register new handlers using the factory or dependency injection.

## Reference
- Patterns and models are inspired by the book and the example codebase.
