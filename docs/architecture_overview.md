# Architecture Overview

This document provides a high-level overview of the event-driven microservices architecture for the project, referencing the principles and examples from "Building Python Microservices with FastAPI".

## Components
- **Web UI**: User-facing frontend.
- **API Gateway (OAuth Client & Event Publisher)**: Handles authentication (Keycloak), publishes events to Redis, and routes API requests.
- **Keycloak**: Central authentication and authorization server.
- **Redis**: Used as both a message broker (for events) and a cache.
- **Microservices**: (e.g., `library_mgt`, `student_mgt`, etc.) Subscribe to events and process them asynchronously.

## Authentication and Event Flow
- The API Gateway is the only component that handles OIDC login and token exchange (see event_driven.md diagram).
- Microservices only validate JWTs and consume events from Redis.
- All requests and event publishing are authenticated and authorized by the Gateway.

## Diagram

```
Web UI → API Gateway → Redis (Broker) → Microservices
           ↓
        Keycloak
```

This architecture enables loose coupling, scalability, and asynchronous processing, while maintaining secure authentication and authorization.
