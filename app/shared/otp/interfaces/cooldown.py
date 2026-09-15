"""
app/shared/otp/interfaces/cooldown.py

Here i will check the cooldown things of otp storing
Like if i will do cooldown or not.
"""

from typing import Protocol


from pydantic import EmailStr


from ..domain.enums import OTPPurpose


class OTPCooldown(Protocol):
    """
    1. is_active()
    2. start()

    This will have the way to know the cooldown status and update this
    """

    def is_active(
        self,
        *,
        identifier: EmailStr,
        purpose: OTPPurpose,
    ) -> bool: ...

    def start(
        self,
        *,
        identifier: EmailStr,
        purpose: OTPPurpose,
        cooldown_seconds: int,
    ) -> None:
        """
        This will start the cooldown here

        validity-> How many time seconds the cooldown will be active
        """
        ...
