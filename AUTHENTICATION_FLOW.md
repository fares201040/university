# Keycloak Authentication Flow: FastAPI Gateway

This document details the authentication flow and configuration for a FastAPI gateway using Keycloak as the OIDC provider, with confidential client support.

---

## 1. Environment Configuration

- All secrets and config are stored in `.env` (never hardcoded).
- Required fields in `.env`:
  - `KEYCLOAK_BASE_URL`: Keycloak server base URL (e.g., http://localhost:8080)
  - `REALM_NAME`: Keycloak realm name
  - `CLIENT_ID`: Keycloak client ID
  - `CLIENT_SECRET`: Keycloak client secret (for confidential clients)
  - `ALGORITHMS`: JWT algorithms (e.g., ["RS256"])
  - `ACCESS_TOKEN_EXPIRE_MINUTES`: Access token lifetime
  - `REFRESH_TOKEN_EXPIRE_MINUTES`: Refresh token lifetime
  - `DEBUG`: Enable debug mode

## 2. Settings Loading (`settings.py`)

- Uses `pydantic-settings` to load all config from `.env`.
- Raises a clear error if any required variable is missing or `.env` cannot be read.
- Example:
  ```python
  class Settings(BaseSettings):
      KEYCLOAK_BASE_URL: str
      REALM_NAME: str
      CLIENT_ID: str
      CLIENT_SECRET: str
      ALGORITHMS: list[str]
      ACCESS_TOKEN_EXPIRE_MINUTES: int
      REFRESH_TOKEN_EXPIRE_MINUTES: int
      DEBUG: bool
      class Config:
          env_file = ".env"
          env_file_encoding = "utf-8"
  try:
      settings = Settings()
  except Exception as e:
      raise RuntimeError("Failed to load settings from .env file. Please ensure all required variables are set.") from e
  ```

## 3. Keycloak Endpoint Construction (`keycloak.py`)

- Endpoints for auth, token, userinfo, and logout are constructed using settings from `.env`.
- Example:
  ```python
  def get_keycloak_config() -> dict:
      base_url = settings.KEYCLOAK_BASE_URL.rstrip("/")
      realm = settings.REALM_NAME
      return {
          "auth_url": f"{base_url}/realms/{realm}/protocol/openid-connect/auth",
          "token_url": f"{base_url}/realms/{realm}/protocol/openid-connect/token",
          "userinfo_url": f"{base_url}/realms/{realm}/protocol/openid-connect/userinfo",
          "logout_url": f"{base_url}/realms/{realm}/protocol/openid-connect/logout",
      }
  ```

## 4. Authentication Flow (`auth.py`)

### a. Login Endpoint
- Generates PKCE code verifier/challenge.
- Redirects user to Keycloak login with PKCE parameters.

### b. Callback Endpoint
- Receives authorization code from Keycloak.
- Exchanges code for tokens at Keycloak token endpoint.
- Uses `CLIENT_SECRET` if present (confidential client):
  ```python
  data = {
      "grant_type": "authorization_code",
      "client_id": settings.CLIENT_ID,
      "code": code,
      "redirect_uri": "http://localhost:8000/auth/callback",
      "code_verifier": code_verifier,
  }
  if hasattr(settings, "CLIENT_SECRET") and settings.CLIENT_SECRET:
      data["client_secret"] = settings.CLIENT_SECRET
  resp = requests.post(token_url, data=data)
  ```
- Sets access and refresh tokens in secure cookies.

### c. JWT Validation
- Validates JWTs using public keys from Keycloak JWKS endpoint.
- Checks audience, issuer, and algorithm.
- Raises error if validation fails.

## 5. Security Best Practices
- Never commit `.env` files with secrets to version control.
- Use secure cookies for tokens.
- Always validate JWTs for protected endpoints.
- Use environment variables for all secrets/config.

---

## 6. How to Test the Authentication Flow

Follow these steps to verify your FastAPI-Keycloak authentication setup:

### 1. Prepare Environment
- Ensure your `.env` file contains all required variables and secrets.
- Start your Keycloak server and confirm the realm, client, and secret match your `.env` values.

### 2. Install Dependencies
- Run:
  ```bash
  pip install -r requirements.txt
  ```

### 3. Start FastAPI Server
- Run:
  ```bash
  uvicorn main:app --reload
  ```
- Confirm the server starts without errors related to missing environment variables.

### 4. Test Login Flow
- Open your browser and navigate to:
  ```
  http://localhost:8000/auth/login
  ```
- You should be redirected to the Keycloak login page.
- Log in with a valid Keycloak user.

### 5. Test Callback and Token Exchange
- After login, you should be redirected to `/auth/callback`.
- The server should exchange the authorization code for tokens.
- Access and refresh tokens should be set in secure cookies.

### 6. Validate JWT
- Access a protected endpoint (e.g., `/some-protected-endpoint`) with the access token.
- The server should validate the JWT and allow access if valid.

### 7. Error Handling
- Remove or corrupt a required variable in `.env` and restart the server.
- Confirm that a clear error is raised and the server does not start.

### 8. Debugging
- If login or token exchange fails, check:
  - Keycloak client type (should be confidential)
  - Client secret matches `.env`
  - Redirect URI matches Keycloak client config
  - Server logs for error details

---

For further details or troubleshooting, see the code comments in each file or contact your system administrator.
