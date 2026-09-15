"""
app/shared/otp/infrastructure/attempts.py

Here i will write the real backend service of how they will have the attempts
"""

from pydantic import EmailStr
from redis import Redis


from ..interfaces.attempts import OTPAttemptTracker  # type: ignore

from ..domain.enums import OTPPurpose


class RedisAttemptTracker:
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
        r = f"otp:attempts:{purpose.value}:{identifier.lower()}"
        return r

    def get_attempt_count(
        self,
        *,
        identifier: EmailStr,
        purpose: OTPPurpose,
    ) -> int:
        """
        This will shows how many attempts has been alreay done
        """
        key = self._make_key(identifier=identifier, purpose=purpose)

        r = self._redis.get(
            name=key,
        )
        if r is None:
            return 0

        r_str = str(r)

        try:
            r_int = int(r_str)
            return r_int

        except (TypeError, ValueError) as exc:
            raise RuntimeError(
                f"Invalid OTP attempt counter stored in Redis "
                f"for key {key!r}: {r_str!r}"
            ) from exc

    # TODO i have some confusion
    # i am returnning 99 as exception which maybe some server error

    def increment(
        self,
        *,
        identifier: str,
        purpose: OTPPurpose,
    ) -> None:
        """
        For wrong attempt it will increment an attmept
        """
        key = self._make_key(
            identifier=identifier,
            purpose=purpose,
        )
        self._redis.incr(key)

    def reset(
        self,
        *,
        identifier: str,
        purpose: OTPPurpose,
    ) -> None:
        """
        This will reset the attempts to 0
        so that after new otp generate the old attempts not counts
        """
        key = self._make_key(
            identifier=identifier,
            purpose=purpose,
        )
        self._redis.delete(key)

    def start(
        self,
        *,
        identifier: str,
        purpose: OTPPurpose,
        ttl_seconds: int,
    ) -> None:
        """
        Thsi will make the attempt_count = 0
        so that it can be auto expired with time of otp expire
        """
        key = self._make_key(
            identifier=identifier,
            purpose=purpose,
        )
        self._redis.set(
            name=key,
            value=0,
            ex=ttl_seconds,
        )


class LocalOTPAttemptTracker:
    """
    This is for locally development for testing purpose only
    """

    DEFAULT_ATTEMPTS = 1

    def get_attempt_count(
        self,
        *,
        identifier: EmailStr,
        purpose: OTPPurpose,
    ) -> int:
        return self.DEFAULT_ATTEMPTS

    def increment(
        self,
        *,
        identifier: str,
        purpose: OTPPurpose,
    ) -> None:
        pass

    def reset(
        self,
        *,
        identifier: EmailStr,
        purpose: OTPPurpose,
    ) -> None:
        pass

    def start(
        self,
        *,
        identifier: str,
        purpose: OTPPurpose,
        ttl_seconds: int,
    ) -> None:
        pass
