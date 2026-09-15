"""
app/features/identity/domain/services/password_hasher.py

My password checking way will be here
"""

from typing import Protocol


class PasswordHasher(Protocol):
    """
    This is the Class is for password checking and do thigns
    """

    def make_hash(self, password: str) -> str: ...
    def verify(self, password: str, hashed_password: str) -> bool: ...
