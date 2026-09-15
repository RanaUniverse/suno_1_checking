"""
app/shared/otp/policy.py

Security realted thigns will be present here
This will keep  the otp policy which will decide how
and what the otp generation will be and how those will be

This is for separate the validity, cooldown and so on for different
purpose of differne otp send type.
"""

from .enums import OTPPurpose
from .models import OTPPolicy

register_policy = OTPPolicy(
    validity=600,
    cooldown=60,
    max_attempts=5,
    length=4,
)

login_policy = OTPPolicy(
    validity=300,
    cooldown=30,
    max_attempts=5,
    length=6,
)

forget_password_policy = OTPPolicy(
    validity=300,
    cooldown=60,
    max_attempts=5,
    length=8,
)


OTP_POLICY_MAP = {
    OTPPurpose.REGISTER: register_policy,
    OTPPurpose.LOGIN: login_policy,
    OTPPurpose.FORGET_PASSWORD: forget_password_policy,
}


def get_otp_policy_obj(
    purpose: OTPPurpose,
) -> OTPPolicy:
    """
    i will run this fun always to get the policy obj
    """

    x = OTP_POLICY_MAP[purpose]
    return x


def validate_otp_policies() -> None:
    """
    This will raise error if not configured all
    """

    missing = [purpose.value for purpose in OTPPurpose if purpose not in OTP_POLICY_MAP]
    if missing:
        raise RuntimeError("Missing OTP Policies For List Of:" f"{missing}")
