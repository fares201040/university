```mermaid
sequenceDiagram
    actor User as User (Resource Owner)
    participant WebUI as Web UI (Frontend)
    participant APIGW as API Gateway (OAuth Client & Event Publisher)
    participant Keycloak as Keycloak (Auth Server)
    participant Broker as Message Broker
    participant MS_A as Microservice A

    User->>WebUI: Clicks "Login"
    WebUI->>APIGW: Redirects to /auth (with PKCE params)
    APIGW->>Keycloak: OAuth2 Auth Request
    Keycloak->>User: Presents login form
    User->>Keycloak: Enters credentials
    Keycloak->>APIGW: Redirect with code
    APIGW->>Keycloak: Token exchange (code, PKCE)
    Keycloak->>APIGW: Returns tokens
    APIGW->>WebUI: Forwards tokens

    WebUI->>APIGW: API Request (with JWT)
    APIGW->>Keycloak: Validate Token (optional)
    APIGW->>Broker: Publish Event (e.g., UserAction)
    MS_A->>Broker: Subscribes to Event
    Broker->>MS_A: Delivers Event
    MS_A->>APIGW: (Optional) Publish Result Event
    APIGW->>WebUI: (Optional) Notify via WebSocket/Callback