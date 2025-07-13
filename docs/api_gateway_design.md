# API Gateway Design

This document explains how the API Gateway acts as both an OAuth client (for authentication) and an event publisher (for event-driven communication).

## Responsibilities
- Authenticate users via Keycloak (OAuth2 Authorization Code Flow).
- Issue and validate JWT tokens.
- Publish events to Redis channels for microservices to consume.
- (Optional) Subscribe to result channels for user notifications.

## Integration with Keycloak
- Handles OAuth2 login, token exchange, and validation.
- Forwards tokens to the Web UI after successful authentication.

## Integration with Redis
- Publishes events to specific channels based on API requests.
- Uses a standard event schema (see `event_schema_and_contracts.md`).
- (Optional) Subscribes to result channels for asynchronous responses.

## Security
- Validates all incoming requests and tokens before publishing events.
- Ensures only authorized users can trigger events.

## Extensibility
- New event types and channels can be added without changing the gateway's core logic.
- Follows OOP and dependency injection principles for maintainability.

## Authentication Flow (OIDC)
- The API Gateway exposes `/auth/login` to redirect users to Keycloak for login (using PKCE for security).
- After successful login, Keycloak redirects to `/auth/callback` on the Gateway, which exchanges the code for tokens.
- The Gateway forwards tokens to the Web UI (via JSON or cookies).
- All subsequent API requests from the Web UI must include the JWT in the Authorization header.
- The Gateway validates JWTs for protected endpoints and publishes events to Redis only for authenticated users.

## Frontend Integration Guidance
- For browser clients, tokens are set in secure, HTTP-only cookies after login.
- For API clients (SPA/mobile), tokens can be returned in JSON and stored in memory or secure storage.
- Always send credentials (cookies) with requests to protected endpoints.
- Use CORS settings to allow frontend origins and credentials.

## Refresh Token Handling
- The callback endpoint sets both access and refresh tokens in cookies.
- You can implement a /auth/refresh endpoint to allow clients to refresh tokens using the refresh token cookie.

## Error Handling
- All authentication endpoints return clear error messages and use secure logging.

## Event-Driven Pattern
- The Gateway is the only entry point for authentication and event publishing.
- Microservices only consume events and validate JWTs (bearer-only, no login or token exchange logic).

## Example Endpoints
- `/auth/login`: Initiates OIDC login (redirects to Keycloak)
- `/auth/callback`: Handles Keycloak callback and token exchange
- `/secure-ping`: Example protected endpoint
- `/event/book/reserve`: Publishes a BookReserved event (JWT required)
