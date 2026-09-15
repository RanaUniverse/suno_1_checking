"""
app/features/identity/application/login/dto.py

Here i will use to defines how my login dto will be
"""

from dataclasses import dataclass

from pydantic import BaseModel

from ...domain.entities.user import UserDomain
from ...domain.enums import (
    LoginStatus,
    LoginOTPStatus,
)


@dataclass(frozen=True)
class LoginIdentity:
    """
    At Least email or phone should be provided
    """

    email: str | None = None
    phone: str | None = None

    def __post_init__(self):
        if self.email is None and self.phone is None:
            raise ValueError("At least one identity must be provided.")


class LoginResult(BaseModel):
    status: LoginStatus
    identity: LoginIdentity | None = None
    full_name: str | None = None


class LoginOTPResult(BaseModel):
    status: LoginOTPStatus
    user: UserDomain | None = None

    @property
    def success(self) -> bool:
        return self.status == LoginOTPStatus.VERIFIED
