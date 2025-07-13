```mermaid
sequenceDiagram
    actor User as User (Resource Owner)
    participant WebUI as Web UI (Frontend)
    participant APIGW as API Gateway (OAuth Client & API Gateway)
    participant Keycloak as Keycloak (Auth Server)
    participant MS_A as Microservice A

    Note over User,MS_A: OAuth 2.0 Authorization Code Flow with API Gateway and Keycloak

    User->>WebUI: Clicks "Login"
    WebUI->>APIGW: Redirects to /auth (with PKCE params)
    APIGW->>Keycloak: GET /openid-connect/auth?response_type=code&client_id=apigw&redirect_uri=...&scope=openid+profile&state=123&code_challenge=XYZ
    Keycloak->>User: Presents login form
    User->>Keycloak: Enters credentials
    Keycloak->>APIGW: 302 Redirect to /callback?code=AUTH_CODE&state=123
    APIGW->>Keycloak: POST /openid-connect/token (code, client_id, code_verifier, grant_type)
    Keycloak->>APIGW: Returns tokens {access_token, id_token, refresh_token}
    APIGW->>WebUI: Forwards tokens (via HTTPS)
    WebUI->>APIGW: API Request (with Authorization: Bearer ACCESS_TOKEN)
    APIGW->>Keycloak: Validate Token (introspect or verify JWT)
    APIGW->>MS_A: Forward request (if valid)
    MS_A->>APIGW: Response (data or error)
    APIGW->>WebUI: Forwards API response
    WebUI->>User: Displays data or error
```

---

### Flow Explanation

- **User Authentication:**
  - The user initiates login from the Web UI, which redirects to the API Gateway.
  - The API Gateway manages the OAuth2 Authorization Code flow with Keycloak, including PKCE for security.
  - Keycloak presents its login form and authenticates the user.
  - Upon successful authentication, Keycloak returns an authorization code to the API Gateway, which exchanges it for tokens.
  - The API Gateway forwards the tokens to the Web UI.

- **API Requests:**
  - The Web UI sends API requests with the access token to the API Gateway.
  - The API Gateway validates the token with Keycloak (via introspection or JWT verification).
  - If valid, the API Gateway forwards the request to Microservice A.
  - Microservice A returns a response to the API Gateway.
  - The API Gateway forwards the response to the Web UI, which displays the result to the user.

- **No Direct Microservice Communication:**
  - Only Microservice A is present; all requests are routed through the API Gateway for clarity and security.

This flow ensures secure, centralized authentication and authorization, and a clear, maintainable architecture for your microservices system.