# Event Schema and Contracts

This document defines the standard event schema, contracts, and versioning for all inter-service communication in the project.

## Event Message Format
- **type**: The event type (e.g., `BookReserved`, `StudentRegistered`).
- **version**: Event schema version (for compatibility).
- **timestamp**: Event creation time (ISO8601).
- **payload**: The event data (JSON object).
- **metadata**: (Optional) Additional info (e.g., correlation ID, user info).

## Example Event
```json
{
  "type": "BookReserved",
  "version": "1.0",
  "timestamp": "2025-07-11T12:00:00Z",
  "payload": {
    "student_id": "123",
    "book_id": "456"
  },
  "metadata": {
    "correlation_id": "abc-123"
  }
}
```

## Event Types & Channels
- `BookReserved` (channel: `book.reserved`)
- `StudentRegistered` (channel: `student.registered`)
- ... (extend as needed)

## Versioning
- Increment the `version` field for breaking changes.
- Maintain backward compatibility where possible.

## Contract Management
- All authentication and token exchange is handled by the API Gateway, following the event-driven diagram.
- Microservices only validate JWTs (bearer-only) and do not handle login or token exchange.
- Events are published to Redis by the Gateway after successful authentication.
- All event types and payloads must be documented here before implementation.
