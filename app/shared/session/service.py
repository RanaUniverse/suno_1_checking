"""
app/shared/session/service.py

Here i will defines the services so that i can talk with session easily

'register_pending': {'email': 'email_id@gmail.com', 'phone': 9876543210}


"""

from typing import Any

from flask import session

from .enums import IdentitySessionKey


def set_key(
    key: Any,
    value: Any,
) -> None:
    """
    Just Store a value in the Flask session.
    """
    session[key] = value


def get_value(key: Any) -> Any | None:
    """
    Get the value form the flask's session
    """

    return session.get(
        key,
        None,
    )


def pop_key(
    key: Any,
) -> Any | None:
    """
    Get and remove a value from the Flask session.
    """
    return session.pop(
        key,
        None,
    )


def set_identity_key(
    key: IdentitySessionKey,
    email_value: str | None = None,
    phone_value: str | None = None,
) -> None:
    """
    I need to pass atleast email or phone value here
    This will just set the key in the session

    At least one of `email_value` or `phone_value` must be provided.

    Args:
        key: Identity session key to store the data under.
        email_value: Email address associated with the identity.
        phone_value: Phone number associated with the identity.

    Raises:
        ValueError: If both email and phone are not provided.
    """
    if email_value is None and phone_value is None:
        raise ValueError(
            "At least email or phone must be provided.",
        )

    data = {
        "email": email_value,
        "phone": phone_value,
    }

    set_key(
        key=key,
        value=data,
    )


def get_identity(
    key: IdentitySessionKey,
) -> dict[str, str | None] | None:
    """
    Get identity information from the session.

    Thsi will return the dict then i can need to fetch what i need
    """
    value = get_value(key)

    if value is None:
        return None

    return value


def get_identity_email(
    key: IdentitySessionKey,
) -> str | None:
    """
    Get the email value from an identity session entry.

    As time of saving the email i validated that email,
    so here i dont need to validate the email from this
    """
    identity = get_identity(
        key,
    )

    if identity is None:
        return None

    return identity.get("email")


def get_identity_phone(
    key: IdentitySessionKey,
) -> str | None:
    """
    Get the phone value from an identity session entry.
    """
    identity = get_identity(key)

    if identity is None:
        return None

    return identity.get("phone")
