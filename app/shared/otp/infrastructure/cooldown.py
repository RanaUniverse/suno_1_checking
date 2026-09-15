"""
app/shared/otp/infrastructure/cooldown.py

This will have the logic only of how to handle the cooldown thigns
"""

from pydantic import EmailStr
from redis import Redis


from ..interfaces.cooldown import OTPCooldown  # type: ignore
from ..domain.enums import OTPPurpose


class RedisCooldown:
    """
    Redis cooldown for opt things will be here

    It doesn't need to have a value, it just need to have
    exists a key to know if the email is in cooldown to send
    email otp again or not.

    For now i will keep the value of "1" to mark it else destroy
    """

    def __init__(
        self,
        redis_client: Redis,
    ) -> None:
        self._redis = redis_client

    def _make_key(
        self,
        *,
        identifier: EmailStr,
        purpose: OTPPurpose,
    ) -> str:
        r = f"otp:cooldown:{purpose.value}:{identifier.lower()}"
        return r

    def is_active(
        self,
        *,
        identifier: EmailStr,
        purpose: OTPPurpose,
    ) -> bool:
        """
        This will check if this cooldown key exists as based on this new
        otp will send to user or not so that user will not ask for otp to frequently
        """
        
        key = self._make_key(
            identifier=identifier,
            purpose=purpose,
        )

        r = self._redis.exists(key)

        return bool(r)

    def start(
        self,
        *,
        identifier: EmailStr,
        purpose: OTPPurpose,
        cooldown_seconds: int,
    ) -> None:
        """
        This will start the cooldown means
        this will keep record that the email has send the otp sometime ago
        so user should not req for another otp till then so i will start
        """

        key = self._make_key(
            identifier=identifier,
            purpose=purpose,
        )
        self._redis.set(
            name=key,
            value="1",  # i keep this value just for key existance chekcing
            ex=cooldown_seconds,
        )


class LocalCooldown:
    """
    This is for local testing cooldown
    it will only give some demo data for local development

    For now this u,v,w gmail are in cooldown those should say in cooldown for sometime
    """

    def __init__(self) -> None:
        x = {
            "u@gmail.com",
            "v@gmail.com",
            "w@gmail.com",
            "rana2@rana.com",
        }
        self._cooldown_identifiers: set[str] = x

    def is_active(
        self,
        *,
        identifier: EmailStr,
        purpose: OTPPurpose,
    ) -> bool:
        x = identifier.lower() in self._cooldown_identifiers
        return x

    def start(
        self,
        *,
        identifier: EmailStr,
        purpose: OTPPurpose,
        cooldown_seconds: int,
    ) -> None:
        """
        This will start the cooldown here
        """
        pass
