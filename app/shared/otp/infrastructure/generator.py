"""
app/shared/otp/infrastructure/generator.py

Here i will have the logic to generate the otp
this values i will call in my send, executes and so on using the factory.py
"""

import secrets
import string


from ..interfaces.generator import OTPGenerator  # type: ignore
from app.config import settings


class LocalTestingOTPGenerator:
    """
    For LOcal testing i mostly not use htis
    """

    def generate(
        self,
        length: int,
    ) -> str:
        if length <= 0:
            raise ValueError("OTP length must be greater than zero.")

        test_otp = settings.otp.test_otp

        if length > len(test_otp):
            raise ValueError(
                f"Local testing OTP supports maximum length " f"{len(test_otp)}."
            )

        return test_otp[:length]


class OTPNumberGenerator:
    """
    This cretes the numeric otp of some length
    """

    def generate(
        self,
        length: int,
    ) -> str:
        # i will use another login in reality #TODO
        if length <= 0:
            raise ValueError("Otp should must be greater than zero.")

        digits = string.digits
        otp = "".join(secrets.choice(digits) for _ in range(length))
        return otp


class OTPAlphabetGenerator:
    """
    This will generate the ALPHABETICAL OTP
    """

    def generate(
        self,
        length: int,
    ) -> str:
        if length <= 0:
            raise ValueError("Otp should must be greater than zero.")

        LETTERS = string.ascii_uppercase
        otp = "".join(secrets.choice(LETTERS) for _ in range(length))
        return otp
