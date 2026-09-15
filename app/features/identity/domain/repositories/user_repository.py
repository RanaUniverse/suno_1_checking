"""
app/features/identity/domain/repositories/user_repository.py

Repository interface
    ↓
"How does my application ask for Users?"

The contract:
   "What can I ask a User repository to do?"
"""

from typing import Protocol


from ..entities.user import UserDomain


class UserRepository(Protocol):
    """
    This is the base class of methods list i will make in my code
    all the other real database implimentation should have folow this
    """

    def get_by_id(self, user_id: str) -> UserDomain | None: ...

    def get_by_email(self, email: str) -> UserDomain | None: ...

    def exists_by_email(self, email: str) -> bool: ...

    def add(self, user: UserDomain) -> UserDomain: ...

    def update_password(self, user: UserDomain, hashed_password:str) -> UserDomain: ...
