"""
app/shared/otp/enums.py

Here i will keep write this other will import this
this module will not import anything
"""

from enum import StrEnum


class OTPPurpose(StrEnum):
    """
    How the differentiate will be between login/register and
    the purpose of the otp generation will be here

    .value will give me the value here defined

    After adding New OTPPurpose i need to check and
    add the email presentation and others cases.
    """

    REGISTER = "register"
    LOGIN = "login"
    FORGET_PASSWORD = "forget_password"
    ORDER_CONFIRMATION = "order_confirmation"


class OTPSendStatus(StrEnum):
    """
    This is an enum class of string
    it will keep note of the otp send
    informaiton if it send or not or anythign
    """

    SENT = "sent"

    COOLDOWN_ACTIVE = "cooldown_active"
    EMAIL_BLOCKED = "email_blocked"
    ATTEMPT_LIMIT_EXCEEDED = "attempt_limit_exceeded"

    EMAIL_SERVER_FAILED = "email_server_failed"
    SEND_FAILED = "send_failed"


class OTPVerifyStatus(StrEnum):
    """
    this will need to call when i will send
    what happens after the otp got received to check
    it will say what actulaly happens by this check
    """

    VERIFIED = "verified"
    INVALID_OTP = "invalid_otp"
    OTP_NOT_FOUND = "otp_not_found"
    ATTEMPT_LIMIT_EXCEEDED = "attempt_limit_exceeded"
