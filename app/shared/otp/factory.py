"""
app/shared/otp/factory.py

Here i will out which otp model i will use in my case
"""

from dataclasses import dataclass


from app.config import settings

from .interfaces.attempts import OTPAttemptTracker
from .interfaces.blocklist import BlockList
from .interfaces.cooldown import OTPCooldown
from .interfaces.generator import OTPGenerator
from .interfaces.storage import OTPStorage

from .infrastructure.attempts import LocalOTPAttemptTracker, RedisAttemptTracker
from .infrastructure.blocklist import LocalInMemoryBlocklist, RedisBlocklist
from .infrastructure.cooldown import LocalCooldown, RedisCooldown
from .infrastructure.generator import OTPNumberGenerator, LocalTestingOTPGenerator
from .infrastructure.storage import LocalTestingOTPStorage, RedisOTPStorage


from ..redis.client import redis_client, validate_redis_connection


def create_otp_generator() -> OTPGenerator:
    if settings.otp.backend == "redis":
        return OTPNumberGenerator()

    return LocalTestingOTPGenerator()


def create_otp_attempt_tracker() -> OTPAttemptTracker:

    if settings.otp.backend == "redis":
        return RedisAttemptTracker(
            redis_client=redis_client,
        )

    return LocalOTPAttemptTracker()


def create_blocklist_email() -> BlockList:
    """
    For now locally development it send later i will use real db
    """

    if settings.otp.backend == "redis":
        return RedisBlocklist(
            redis_client=redis_client,
        )
    return LocalInMemoryBlocklist()


def create_otp_cooldown() -> OTPCooldown:

    if settings.otp.backend == "redis":
        return RedisCooldown(
            redis_client=redis_client,
        )

    return LocalCooldown()


def create_otp_storage() -> OTPStorage:

    if settings.otp.backend == "redis":
        return RedisOTPStorage(
            redis_client=redis_client,
        )

    return LocalTestingOTPStorage()


# I keep upper fun differntly here so that i can change any logic
# if i want to change any component there


@dataclass(
    frozen=True,
)
class OTPComponents:
    storage: OTPStorage
    generator: OTPGenerator
    cooldown: OTPCooldown
    attempt: OTPAttemptTracker
    blocklist: BlockList


def create_otp_components() -> OTPComponents:
    """
    This is creating all the necessary otp related objects
    i will use those values as dependency injection in my usecase
    """

    if settings.otp.backend == "redis":
        validate_redis_connection()

    attempt_tracker_obj = create_otp_attempt_tracker()
    cooldown_obj = create_otp_cooldown()
    generator_obj = create_otp_generator()
    storage_obj = create_otp_storage()
    blocklist_email_obj = create_blocklist_email()

    return OTPComponents(
        storage=storage_obj,
        generator=generator_obj,
        cooldown=cooldown_obj,
        attempt=attempt_tracker_obj,
        blocklist=blocklist_email_obj,
    )


otp_componenet_objects = create_otp_components()
