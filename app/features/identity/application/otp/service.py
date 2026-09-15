"""
app/features/identity/application/registration/otp.py


Identity specefic OTP operations.

Here i will write my otp related services
Like how it will call otp generate, verifications and so on
"""

from pydantic import EmailStr


from app.shared.otp.services.send import OTPSendService
from app.shared.otp.services.verify import OTPVerifyService

from app.shared.otp.domain.models import (
    OTPSendResult,
    OTPVerifyResult,
)

from app.shared.otp.factory import (
    otp_componenet_objects,
)

from app.shared.mail.factory import mail_sender_obj

from app.shared.otp.domain.enums import (
    OTPPurpose,
)


def send_otp_to_email(
    email_id: EmailStr,
    purpose: OTPPurpose,
) -> OTPSendResult:
    """
    I will add Celery here which will send email later

    Here i need to pass the correct validated email id
    which is not register/login or what so ever in the database and then
    it will just try to send otp to him
    """

    s = OTPSendService(
        attempt=otp_componenet_objects.attempt,
        cooldown=otp_componenet_objects.cooldown,
        generator=otp_componenet_objects.generator,
        storage=otp_componenet_objects.storage,
        blocklist=otp_componenet_objects.blocklist,
        sender=mail_sender_obj,
    )

    mail_send = s.execute(
        identifier=email_id,
        purpose=purpose,
    )

    return mail_send


def verify_otp_against_email(
    email: EmailStr,
    purpose: OTPPurpose,
    submitted_otp: str,
) -> OTPVerifyResult:
    """
    This will take the email_id and then validate those
    against the otp given by the user
    """

    s = OTPVerifyService(
        attempt=otp_componenet_objects.attempt,
        storage=otp_componenet_objects.storage,
    )

    otp_checking = s.execute(
        identifier=email,
        purpose=purpose,
        submitted_otp=submitted_otp,
    )

    return otp_checking
