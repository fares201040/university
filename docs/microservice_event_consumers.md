# Microservice Event Consumers

This document details how each microservice subscribes to and processes events from Redis, following OOP and scalable design principles.

## Responsibilities
- Subscribe to relevant Redis channels for event types (e.g., `book.reserved`).
- Process events asynchronously in background workers.
- (Optional) Publish result events to Redis for further processing or notifications.

## OOP Patterns
- Use a base event consumer class for shared logic (connection, subscription, error handling).
- Subclass for each microservice to handle specific event types and business logic.
- Use dependency injection for configuration and event handlers.

## Scalability
- Multiple instances of each microservice can consume from the same channel for horizontal scaling.
- Event processing should be idempotent to handle retries.

## Extensibility
- New event types can be handled by adding new handler methods or subclasses.

## Example
- `library_mgt` subscribes to `book.reserved` and processes book reservation events.
- `student_mgt` subscribes to `student.registered` and processes student registration events.
