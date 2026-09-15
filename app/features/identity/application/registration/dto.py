"""
app/features/identity/models.py

This will have the models or data to keep for this related thigns
"""

from dataclasses import dataclass


from pydantic import BaseModel

from ...domain.entities.user import UserDomain

from ...domain.enums import (
    RegistrationStatus,
    AfterRegistrationNextStep,
    RegistrationOTPStatus,
    RegistrationOTPStatusNextStep,
)


@dataclass(frozen=True)
class RegistrationIdentity:
    """
    At Least email or phone should be provided
    """

    email: str | None = None
    phone: str | None = None

    def __post_init__(self):
        if self.email is None and self.phone is None:
            raise ValueError("At least one identity must be provided.")


class RegistrationStartingResult(BaseModel):
    """
    This is for Frontend, this result will use by routes.py
    to check where to redirect the user based on the result
    """

    status: RegistrationStatus
    next_step: AfterRegistrationNextStep
    identity: RegistrationIdentity | None = None

    @property
    def success(
        self,
    ) -> bool:
        """
        This say true if the registration mail has sent to user
        successfully. maybe mail has dispatched then it will true
        """

        x = self.status == RegistrationStatus.OTP_SENT
        return x


class RegistrationViaOTPResult(BaseModel):
    """
    I will next_step = none when this will be decide by the routes.py
    """

    status: RegistrationOTPStatus
    user: UserDomain | None = None
    next_step: RegistrationOTPStatusNextStep | None = None

    @property
    def success(
        self,
    ) -> bool:
        """
        This will say true if register has the status of success
        """
        r = self.status == RegistrationOTPStatus.VERIFIED
        return r
