"""
app/shared/otp/verify.py

This is responsible to verify the otp agaist the input
given by the user
"""

from pydantic import EmailStr


from ..domain.enums import OTPPurpose, OTPVerifyStatus
from ..domain.models import OTPVerifyResult
from ..domain.policy import get_otp_policy_obj

from ..interfaces.storage import OTPStorage
from ..interfaces.attempts import OTPAttemptTracker


class OTPVerifyService:
    """
    This will check if the otp is matched with other validation
    and it will do all the checkup and cleanup also
    """

    def __init__(
        self,
        attempt: OTPAttemptTracker,
        storage: OTPStorage,
    ) -> None:
        self._attempt = attempt
        self._storage = storage

    def execute(
        self,
        identifier: EmailStr,
        purpose: OTPPurpose,
        submitted_otp: str,
    ) -> OTPVerifyResult:

        policy_obj = get_otp_policy_obj(
            purpose=purpose,
        )

        attempt_count = self._attempt.get_attempt_count(
            identifier=identifier,
            purpose=purpose,
        )

        if attempt_count >= policy_obj.max_attempts:
            return OTPVerifyResult(
                status=OTPVerifyStatus.ATTEMPT_LIMIT_EXCEEDED,
                message="Maximum otp verificion attempts exceed",
            )

        stored_otp = self._storage.get_otp(
            identifier=identifier,
            purpose=purpose,
        )

        if stored_otp is None:
            return OTPVerifyResult(
                status=OTPVerifyStatus.OTP_NOT_FOUND,
                message="No OTP is found maybe not exists or expired",
            )

        if submitted_otp != stored_otp:
            self._attempt.increment(
                identifier=identifier,
                purpose=purpose,
            )
            return OTPVerifyResult(
                status=OTPVerifyStatus.INVALID_OTP,
                message="OTP Does not matched.",
            )

        # now this line came measn otp got matched now i will remove this from storage
        self._storage.delete_otp(
            identifier=identifier,
            purpose=purpose,
        )
        self._attempt.reset(
            identifier=identifier,
            purpose=purpose,
        )
        return OTPVerifyResult(
            status=OTPVerifyStatus.VERIFIED,
            message="OTP Got Matched now",
        )
