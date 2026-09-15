"""
app/features/identity/infrastructure/mongo/user_repository.py

Here i will write mongo related thigns if i will use later
but this is for demo for now
"""

# i am using the below class as a protocol to make this below
# from ...domain.repositories.user_repository import UserRepository
from ...domain.entities.user import UserDomain


class MongoDBUserRepository:
    def __init__(self) -> None:
        pass

    def get_by_id(self, user_id: str) -> UserDomain | None: ...

    def get_by_email(self, email: str) -> UserDomain | None: ...

    def exists_by_email(self, email: str) -> bool: ...

    def add(self, user: UserDomain) -> UserDomain: ...

    def update_password(self, user: UserDomain, hashed_password: str) -> UserDomain: ...
