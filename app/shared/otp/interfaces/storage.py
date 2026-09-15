"""
app/shared/otp/interfaces/storage.py

This is for OTP Storage Things will be here
"""

from typing import Protocol


from ..domain.enums import OTPPurpose


class OTPStorage(Protocol):
    """
    1. save_otp()
    2. get_otp()
    3. delete_otp()

    This will have all the otp related thigns to know by this
    like cooldown, generate or expire how works with its methods.

    This is My Business Logic of When & How to Send or Limit the
    OTP Sending to the user.

    I will use Redis, or DB later which i need to impliment below methods.
    """

    def save_otp(
        self,
        *,
        identifier: str,
        purpose: OTPPurpose,
        otp: str,
        ttl_seconds: int,
    ) -> None:
        """
        This should to save the otp so that later i can check

        ttl-seconds: How long time the otp will be validate then it will invalid
        """
        ...

    def get_otp(
        self,
        *,
        identifier: str,
        purpose: OTPPurpose,
    ) -> str | None:
        """
        This will try to read the otp from my backend
        whcih was store in some place
        """
        ...

    def delete_otp(
        self,
        *,
        identifier: str,
        purpose: OTPPurpose,
    ) -> None:
        """
        It will try to delete the otp from cache if it need to remove beforehand
        or if this has validate it need to be delete so that noone will complain against this
        """
        ...
