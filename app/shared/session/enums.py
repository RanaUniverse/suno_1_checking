"""
app/shared/session/enums.py

"""

from enum import StrEnum


class IdentitySessionKey(StrEnum):
    REGISTER_PENDING = "register_pending"
    LOGIN_PENDING = "login_pending"
