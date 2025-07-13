# events/README.md

This package contains shared event models and base classes for event-driven communication in the project.

## Contents
- `models.py`: Defines the base `Event` class and example event subclasses.
- `base.py`: Provides abstract base classes for event producers and consumers, and a factory for event handler registration.

## Usage
- Import and extend the `Event` class for new event types.
- Implement `EventProducer` and `EventConsumer` in your gateway and microservices.
- Use `EventHandlerFactory` to register and retrieve event handlers by type.

## Reference
- Patterns and code are inspired by "Building Python Microservices with FastAPI" and the example codebase.
