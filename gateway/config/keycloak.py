from gateway.config.settings import settings

# Settings will be loaded from environment variables if present (via .env file)


def get_keycloak_config() -> dict:
    """Return Keycloak configuration endpoints for OIDC discovery and authentication."""
    base_url = settings.KEYCLOAK_BASE_URL.rstrip("/")
    realm = settings.REALM_NAME
    auth_url = f"{base_url}/realms/{realm}/protocol/openid-connect/auth"
    token_url = f"{base_url}/realms/{realm}/protocol/openid-connect/token"
    userinfo_url = f"{base_url}/realms/{realm}/protocol/openid-connect/userinfo"
    logout_url = f"{base_url}/realms/{realm}/protocol/openid-connect/logout"
    return {
        "auth_url": auth_url,
        "token_url": token_url,
        "userinfo_url": userinfo_url,
        "logout_url": logout_url,
        "base_url": base_url,
        "realm": realm,
    }
