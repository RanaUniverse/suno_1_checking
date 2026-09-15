"""
app/shared/otp/interfaces/blocklist.py

Here i will keep the logic to check blocklisted user to send email
i will for now check by a turn off or on feature and then i will check in execute
"""

from typing import Protocol


from pydantic import EmailStr


class BlockList(Protocol):
    """
    1. is_blocked()

    I think to use a set in redis so that i can use this
    and do block and unblock the users

    Here i will want to have block some user or not
    and then also return if a user is blocked or not
    """

    def is_blocked(
        self,
        identifier: EmailStr,
    ) -> bool:
        """
        For now i am only using Email Address later i will use the
        sms, whatsapp, tg like otp validation

        It should check if the email is in blocked or not
        """
        ...
