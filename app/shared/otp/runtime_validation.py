"""
app/shared/otp/runtime_validation.py

This is where my validation will works of otp realted thigns
"""

from .domain.policy import validate_otp_policies
from .render import validate_otp_email_presentation

from app.config import settings

from .factory import otp_componenet_objects
from .infrastructure.blocklist import RedisBlocklist


def insert_demo_email_in_otp_blocklist_redis():
    # i will insert htis values as blocked user as demo
    print("Adding Some Demo data in redis otp blocklist emails")

    demo_blocked_users: set[str] = {
        "x@gmail.com",
        "y@gmail.com",
        "z@gmail.com",
        "rana1@rana.com",
    }
    blocklist = otp_componenet_objects.blocklist

    if not isinstance(blocklist, RedisBlocklist):
        raise RuntimeError(
            "Development OTP blocklist seeding requires " "RedisBlocklist."
        )

    blocklist.set_some_demo_users_to_blocklist(
        users=demo_blocked_users,
    )


def validate_all_otp_config() -> None:
    """
    This will call all otp realted validation fun and run here
    """
    validation_mode = settings.app.validation_mode

    if validation_mode == "PRODUCTION":

        validate_otp_policies()
        validate_otp_email_presentation()

    elif validation_mode == "DEVELOPMENT":

        # insert_demo_email_in_otp_blocklist_redis()

        r = "This is in Development Now no validation is running."
        print("---")
        print(r)
        print("---")

    else:
        raise RuntimeError(
            "This is wrong validation_mode",
        )
