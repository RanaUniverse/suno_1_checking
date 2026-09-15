"""
app/shared/otp/interfaces/generator.py

"""

from typing import Protocol


class OTPGenerator(Protocol):
    """
    1. generate()

    This will only know the logic to generate the otp
    of a current length
    """

    def generate(
        self,
        length: int,
    ) -> str: ...
