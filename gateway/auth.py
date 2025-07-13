import base64
import hashlib
import secrets
import time
import urllib.parse
from typing import Any, Dict

import requests
from fastapi import APIRouter, Depends, HTTPException, Request, Security, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, RedirectResponse, Response
from jose import JWTError, jwt

from gateway.config.keycloak import get_keycloak_config
from gateway.config.settings import settings

# --- OIDC Discovery ---
keycloak_config = get_keycloak_config()


def fetch_oidc_config() -> dict:
    """Fetch OIDC configuration from Keycloak well-known endpoint."""
    resp = requests.get(
        keycloak_config["auth_url"].replace(
            "/auth", "/.well-known/openid-configuration"
        )
    )
    resp.raise_for_status()
    return resp.json()


oidc_config = fetch_oidc_config()


# --- JWKS Caching & Refresh ---
_jwks_cache = None
_jwks_cache_time = 0
JWKS_CACHE_TTL = 3600  # seconds


def get_jwks() -> dict:
    global _jwks_cache, _jwks_cache_time
    now = time.time()
    if _jwks_cache and (now - _jwks_cache_time < JWKS_CACHE_TTL):
        return _jwks_cache
    resp = requests.get(oidc_config["jwks_uri"])
    resp.raise_for_status()
    _jwks_cache = resp.json()
    _jwks_cache_time = now
    return _jwks_cache


# --- PKCE S256 ---
def generate_pkce_challenge(verifier: str) -> str:
    digest = hashlib.sha256(verifier.encode()).digest()
    return base64.urlsafe_b64encode(digest).rstrip(b"=").decode("ascii")


# --- Modular JWT Validation ---
def extract_public_key_from_jwt(token: str) -> str:
    jwks = get_jwks()
    unverified_header = jwt.get_unverified_header(token)
    for key in jwks["keys"]:
        if key["kid"] == unverified_header["kid"]:
            return jwt.algorithms.RSAAlgorithm.from_jwk(key)
    raise HTTPException(status_code=401, detail="Public key not found")


# Utility to validate JWTs for resource endpoints (bearer-only)
def validate_jwt_token(token: str) -> dict:
    try:
        public_key = extract_public_key_from_jwt(token)
        payload = jwt.decode(
            token,
            public_key,
            algorithms=settings.ALGORITHMS,
            audience=settings.CLIENT_ID,
            issuer=f"{settings.KEYCLOAK_BASE_URL}/realms/{settings.REALM_NAME}",
        )
        return payload
    except JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        ) from e


# Dependency for resource endpoints
def require_jwt_auth(request: Request) -> dict:
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(
            status_code=401, detail="Missing or invalid Authorization header"
        )
    token = auth_header.split(" ", 1)[1]
    return validate_jwt_token(token)


router = APIRouter()


# PKCE helper functions
def generate_pkce_pair() -> tuple[str, str]:
    code_verifier = secrets.token_urlsafe(64)
    code_challenge = generate_pkce_challenge(code_verifier)
    return code_verifier, code_challenge


@router.get("/auth/login")
def login(request: Request) -> Response:
    code_verifier, code_challenge = generate_pkce_pair()
    # Store code_verifier in session (cookie for demo)
    response = RedirectResponse(url="/")  # Placeholder
    response.set_cookie("code_verifier", code_verifier, httponly=True)
    params = {
        "client_id": settings.CLIENT_ID,
        "response_type": "code",
        "scope": "openid profile email",
        "redirect_uri": "http://localhost:8000/auth/callback",
        "code_challenge": code_challenge,
        "code_challenge_method": "S256",
    }
    url = f"{oidc_config['authorization_endpoint']}?{urllib.parse.urlencode(params)}"
    response = RedirectResponse(url)
    response.set_cookie("code_verifier", code_verifier, httponly=True)
    return response


# Add CORS middleware for authentication endpoints
origins = [
    "http://localhost:3000",
    "http://localhost:8000",
]  # Add your frontend origins


def add_cors(app) -> None:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


@router.get("/auth/callback")
def auth_callback(request: Request, code: str) -> Response:
    code_verifier = request.cookies.get("code_verifier")
    if not code_verifier:
        return JSONResponse(
            status_code=400,
            content={
                "error": "Missing code_verifier. Please retry login. This may be a browser/cookie issue or session expired."
            },
        )
    token_url = oidc_config["token_endpoint"]
    data = {
        "grant_type": "authorization_code",
        "client_id": settings.CLIENT_ID,
        "code": code,
        "redirect_uri": "http://localhost:8000/auth/callback",
        "code_verifier": code_verifier,
    }
    # Add client_secret if present (confidential client)
    if hasattr(settings, "CLIENT_SECRET") and settings.CLIENT_SECRET:
        data["client_secret"] = settings.CLIENT_SECRET
    resp = requests.post(token_url, data=data)
    if resp.status_code != 200:
        return JSONResponse(
            status_code=400,
            content={
                "error": "Token exchange failed with Keycloak.",
                "details": resp.text,
                "hint": "Check Keycloak client config, code_verifier, and PKCE setup.",
            },
        )
    tokens = resp.json()
    # Optionally, return tokens in JSON for API clients
    response = JSONResponse(content=tokens)
    response.set_cookie(
        "access_token", tokens.get("access_token", ""), httponly=True, secure=True
    )
    response.set_cookie(
        "refresh_token", tokens.get("refresh_token", ""), httponly=True, secure=True
    )
    response.headers["Access-Control-Allow-Credentials"] = "true"
    return response


# Usage in FastAPI endpoint:
# @app.post("/some-protected-endpoint")
# async def some_endpoint(payload=Depends(require_jwt_auth)):
#     ...
