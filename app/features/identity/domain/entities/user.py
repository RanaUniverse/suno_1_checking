"""
app/features/identity/domain/entities/user.py

Domain User
    ↓
"What is a User in my business?"


suppose in my database i have many 30 columns.

"So I have to put all 30 fields into domain/entities/user.py?"

Not necessarily.

The domain entity should contain the information that is meaningful to your business/domain behavior.

Thsi i keep the validation in past service so here i keep only the necessry thigns

"""

from dataclasses import dataclass


@dataclass
class UserDomain:
    """
    This is my application user this only knows about my business need
    """

    # the value is None when generating but when coming from db this
    # value is present so i keep str|NOne
    email: str

    full_name: str | None = None

    hashed_password: str | None = None
    id_: str | None = None

    is_active: bool = True
    is_verified: bool = False

    def verify(self) -> None:
        """
        This will verify the user
        """
        self.is_verified = True

    def deactivate(self) -> None:
        """
        Make the user deactive
        """
        self.is_active = False

    def activate(self) -> None:
        """
        Make the user as active
        """
        self.is_active = True
