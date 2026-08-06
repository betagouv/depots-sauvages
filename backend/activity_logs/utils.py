def resolve_auth_method(request) -> str:
    """Detect authentication method from session auth user backend."""
    if not request or not hasattr(request, "session"):
        return "inconnu"

    backend = request.session.get("_auth_user_backend", "")
    if "ProConnectOIDCBackend" in backend:
        return "proconnect"
    if "BypassAuthBackend" in backend:
        return "demo"
    return "password"
