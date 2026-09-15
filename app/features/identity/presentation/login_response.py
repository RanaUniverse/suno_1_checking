"""
app/features/identity/presentation/login_response.py

"""

from ..application.login.dto import LoginResult


def get_required_email(
    result: LoginResult,
) -> str | None:
    if result.identity is None:
        return None

    return result.identity.email
