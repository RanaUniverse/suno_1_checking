"""
app/shared/otp/infrastructure/cooldown.py

Here i will write the code to store otp thigns in reality how
it maybe redis, db or somethigns
"""

from redis import Redis


from ..domain.enums import OTPPurpose
from ..interfaces.storage import OTPStorage  # type: ignore

from app.config import settings


class RedisOTPStorage:
    """
    I will use this in relaity to handle the otp by the redis

    Redis will store otp and ttl remove and so on i will follow the
    upper protocol class in this case
    """

    def __init__(
        self,
        redis_client: Redis,
    ) -> None:
        self._redis = redis_client

    def _make_key(
        self,
        *,
        identifier: str,
        purpose: OTPPurpose,
    ) -> str:
        """
        This will make the key here so that in differnet place i can use this easily
        """
        r = f"otp:{purpose.value}:{identifier.lower()}"
        return r

    def save_otp(
        self,
        *,
        identifier: str,
        purpose: OTPPurpose,
        otp: str,
        ttl_seconds: int,
    ) -> None:
        """
        From identifier & purpose i will make the key
        otp_value will be saved as the key value

        identifier is like email id
        Its work is to save the otp in the redis so that i can get the value later
        """

        key = self._make_key(
            identifier=identifier,
            purpose=purpose,
        )

        self._redis.set(
            name=key,
            value=otp,
            ex=ttl_seconds,
        )

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

        key = self._make_key(
            identifier=identifier,
            purpose=purpose,
        )

        r = self._redis.get(
            name=key,
        )

        if r:
            return str(r)
        else:
            return None

    def delete_otp(
        self,
        *,
        identifier: str,
        purpose: OTPPurpose,
    ) -> None:
        """
        i will jsut delete the key from the redis storage
        """
        key = self._make_key(
            identifier=identifier,
            purpose=purpose,
        )
        self._redis.delete(
            key,
        )


class LocalTestingOTPStorage:

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
        """
        pass

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
        return settings.otp.test_otp[:4]

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
        pass
