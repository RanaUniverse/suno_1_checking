"""
app/shared/otp/infrastructure/blocklist.py

i will make real implimentation here of real logics here
"""

from pydantic import EmailStr
from redis import Redis

from ..interfaces.blocklist import BlockList  # type: ignore


class RedisBlocklist:
    """
    Redis blocklist now i am just developing this as a checking

    This will keep track recored of the email which are blocked to use the service
    later i will switch to real db to fetch the blocked mails and then set those
    """

    KEY = "otp:blocklist"

    def __init__(
        self,
        redis_client: Redis,
    ) -> None:

        self._redis = redis_client

    def set_some_demo_users_to_blocklist(
        self,
        users: set[EmailStr] | None,
    ):
        if not users:
            return None

        normalized_users = [user.lower() for user in users]

        self._redis.sadd(self.KEY, *normalized_users)

    def is_blocked(
        self,
        identifier: EmailStr,
    ) -> bool:
        """
        only for now check the list of the emails i write here
        """
        r = self._redis.sismember(
            name=self.KEY,
            value=identifier.lower(),
        )

        return bool(r)


class LocalInMemoryBlocklist:
    """
    This is for local testing only i will use for learning purpose only

    Here i keep some local emails to block them.
    """

    def __init__(self) -> None:
        x = {
            "x@gmail.com",
            "y@gmail.com",
            "z@gmail.com",
            "rana1@rana.com",
        }
        self._blocked_identifiers: set[str] = x

    def is_blocked(
        self,
        identifier: EmailStr,
    ) -> bool:
        """
        only for now check the list of the emails i write here
        """
        x = identifier.lower() in self._blocked_identifiers
        return x
