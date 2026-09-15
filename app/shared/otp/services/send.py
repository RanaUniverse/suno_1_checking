"""
app/shared/otp/send.py

This is for send otp to the user over a network

i will move this to my business logic in routes side

#TODO
Later i will do email dispatcher so that my routes will
not wait for the email has send successfully or not
"""

from datetime import datetime


from pydantic import EmailStr


from app.config import settings

from ..domain.enums import OTPPurpose, OTPSendStatus
from ...mail.interfaces.sender import EmailSender
from ...mail.models import EmailMessageData
from ..domain.models import OTPSendResult
from ..render import render_otp_email
from ..domain.policy import get_otp_policy_obj

from ..interfaces.attempts import OTPAttemptTracker
from ..interfaces.blocklist import BlockList
from ..interfaces.cooldown import OTPCooldown
from ..interfaces.generator import OTPGenerator
from ..interfaces.storage import OTPStorage


class OTPSendService:
    """
    For Now OTP is just send over Email
    The otp will send over email,
    This will take the things and then execute
    will send the mail to the user

    Not over other Sender way, i will think later about those
    """

    def __init__(
        self,
        attempt: OTPAttemptTracker,
        cooldown: OTPCooldown,
        generator: OTPGenerator,
        storage: OTPStorage,
        sender: EmailSender,
        blocklist: BlockList,
    ) -> None:
        self._attempt = attempt
        self._cooldown = cooldown
        self._generator = generator
        self._storage = storage
        self._sender = sender
        self._blocklist = blocklist

    def execute(
        self,
        identifier: EmailStr,
        purpose: OTPPurpose,
    ) -> OTPSendResult:
        """
        This will check if otp will send or not by calling the shared/otp related things

        1. Check Cooldown
        2. Generate OTP
        3. clear old cooldown
        """
        # First it will check if this email is block for response for sometime or not
        # if not block it will then try to send the otp to the user
        # TODO

        if self._blocklist.is_blocked(
            identifier=identifier,
        ):
            return OTPSendResult(
                status=OTPSendStatus.EMAIL_BLOCKED,
                message="This Email is Blocked ",
            )

        if self._cooldown.is_active(
            identifier=identifier,
            purpose=purpose,
        ):
            return OTPSendResult(
                status=OTPSendStatus.COOLDOWN_ACTIVE,
                message="Cooldown is Active Now Wait until cooldown expires",
            )

        otp_policy_obj = get_otp_policy_obj(
            purpose=purpose,
        )

        # otp = self._generator.generate(
        #     length=otp_policy_obj.length,
        # )
        print(f"OTP Is Generating At {datetime.now()}...")
        otp = self._generator.generate(
            length=otp_policy_obj.length,
        )
        print("AFTER GENERATOR->", otp)

        self._storage.save_otp(
            identifier=identifier,
            purpose=purpose,
            otp=otp,
            ttl_seconds=otp_policy_obj.validity,
        )

        # self._attempt.reset(
        #     identifier=identifier,
        #     purpose=purpose,
        # )

        self._attempt.start(
            identifier=identifier,
            purpose=purpose,
            ttl_seconds=otp_policy_obj.cooldown,
        )

        self._cooldown.start(
            identifier=identifier,
            purpose=purpose,
            cooldown_seconds=otp_policy_obj.cooldown,
        )

        # TODO
        # later i will make this to the celry to call this later
        mail_data = render_otp_email(
            otp=otp,
            valid_seconds=otp_policy_obj.validity,
            purpose=purpose,
        )
        mail_sub = mail_data.subject
        body_text = mail_data.body_text
        body_html = mail_data.body_html
        # i will call this from the templates.py to genreeat this body
        email_data = EmailMessageData(
            to_email=[
                identifier,
            ],
            subject=mail_sub,
            body_text=body_text,
            body_html=body_html,
            reply_to=settings.mail.address.reply_to_otp,
        )
        self._sender.send_mail(
            email_msg=email_data,
        )
        return OTPSendResult(
            status=OTPSendStatus.SENT,
            message="OTP Request Has Successfully Sended to Email Server.",
        )
