"""
app/features/identity/presentation.py
app/features/identity/presentation/message.py

This say how the UI will displayed.

This is for taking the data from the service and make this
to usable ui text to shows to user via routes.py
"""

from pydantic import BaseModel


from ..domain.enums import RegistrationStatus
from ..application.registration.dto import RegistrationStartingResult

from app.shared.frontend.enums import FlashCategory


class PresentationMessageFlask(BaseModel):
    message: str
    category: FlashCategory = FlashCategory.INFO


def registration_to_flash(
    result: RegistrationStartingResult,
) -> PresentationMessageFlask:
    """
    This will take the result of the service.py and make this
    shows the message to the user to shows in the ui
    """

    messages = {
        RegistrationStatus.OTP_SENT: PresentationMessageFlask(
            message="🎉 OTP sent successfully! Please check your email "
            "and enter the OTP to continue.",
            category=FlashCategory.SUCCESS,
        ),
        RegistrationStatus.EMAIL_ALREADY_REGISTERED: PresentationMessageFlask(
            message="📧 This email is already registered. Please log in using your "
            "password or choose the OTP login option instead.",
            category=FlashCategory.PRIMARY,
        ),
        RegistrationStatus.EMAIL_BLOCKED: PresentationMessageFlask(
            message="🚫 This email address is currently blocked. Please "
            "contact support if you believe this is a mistake.",
            category=FlashCategory.DANGER,
        ),
        RegistrationStatus.OTP_COOLDOWN_ACTIVE: PresentationMessageFlask(
            message="⏳ An OTP was recently sent to your email. Please wait "
            "a little before requesting another one.",
            category=FlashCategory.WARNING,
        ),
        RegistrationStatus.ATTEMPT_LIMIT_EXCEED: PresentationMessageFlask(
            message="⚠️ You've reached the maximum number of registration "
            "attempts. Please try again later.",
            category=FlashCategory.WARNING,
        ),
        RegistrationStatus.EMAIL_SERVICE_FAILED: PresentationMessageFlask(
            message="📨 We couldn't send the OTP email right now. Please try "
            "again in a few moments.",
            category=FlashCategory.DANGER,
        ),
    }

    x = messages.get(
        result.status,
        PresentationMessageFlask(
            message="❌ Something went wrong while processing your registration. Please try again. Pls Report The Admin",
            category=FlashCategory.DANGER,
        ),
    )

    return x

    # i keep this as a safety net so that later i can use this easily
    raise RuntimeError(
        f"Unhandled registration status: {result.status}",
    )
