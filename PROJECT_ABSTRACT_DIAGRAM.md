```mermaid
flowchart TD
    subgraph Clients
        WebUI["Web UI"]
    end
    APIGW["API Gateway (OAuth Client & Event Publisher)"]
    Keycloak["Keycloak (Auth Server)"]
    Broker["Message Broker"]
    MS_A["Microservice A (Event Consumer)"]

    %% User authentication flow
    WebUI -- "Login/Authenticate" --> APIGW
    APIGW -- "OAuth2 Auth Request" --> Keycloak
    Keycloak -- "Auth Response (JWT)" --> APIGW
    APIGW -- "Tokens (JWT)" --> WebUI

    %% API request flow
    WebUI -- "API Request (JWT)" --> APIGW
    APIGW -- "Validate Token" --> Keycloak
    APIGW -- "Publish Event" --> Broker
    MS_A -- "Subscribes/Consumes Event" --> Broker

    %% Optional: Result event flow
    MS_A -- "(Optional) Publish Result Event" --> Broker
    APIGW -- "(Optional) Notify Web UI" --> WebUI
```

---

### Architecture Explanation

- **API Gateway (OAuth Client & Event Publisher):**
  - Handles authentication with Keycloak and issues tokens to the Web UI.
  - Publishes events to the message broker instead of making direct HTTP calls to microservices.
- **Message Broker:**
  - Decouples the API Gateway from Microservice A.
  - Delivers events asynchronously to subscribed microservices.
- **Microservice A (Event Consumer):**
  - Subscribes to relevant events from the broker and processes them.
  - Can publish result events if needed, which the API Gateway can consume to notify the Web UI.
- **Web UI:**
  - Authenticates and communicates only with the API Gateway.
  - Receives notifications or results via the API Gateway (using WebSockets, polling, or callbacks).

This event-driven architecture enables loose coupling, scalability, and asynchronous processing, while maintaining secure authentication and authorization with Keycloak.
