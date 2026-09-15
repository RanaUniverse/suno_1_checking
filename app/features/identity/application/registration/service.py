"""
app/features/identity/services/registration.py

Registration related code fun and so on will be present here

start, resend_otp have duplicaion i need to remove those
#TODO
"""

from pydantic import EmailStr


from app.shared.otp.domain.enums import (
    OTPPurpose,
    OTPSendStatus,
    OTPVerifyStatus,
)

from ...domain.value_objects.email_validation import ValidatedEmail
from ...domain.exceptions import InvalidEmailError

from ...domain.services.password_hasher import PasswordHasher


from ...domain.enums import (
    AfterRegistrationNextStep,
    RegistrationOTPStatus,
    RegistrationStatus,
)

from .dto import (
    RegistrationStartingResult,
    RegistrationViaOTPResult,
    RegistrationIdentity,
)


from ...domain.repositories.user_repository import UserRepository
from ...domain.entities.user import UserDomain

from ..otp.service import send_otp_to_email, verify_otp_against_email


class RegistrationService:
    """
    This will have all the registration related things
    fucntion and checking form this

    The user_repository valeu will come as dependency
    otp_service -> as a di so that it will know how to send
    """

    def __init__(
        self,
        user_repository: UserRepository,
        password_hasher: PasswordHasher,
    ) -> None:

        self._password_hasher = password_hasher
        self._user_repository = user_repository

    def _add_user_to_db(
        self,
        email: EmailStr,
        hashed_password: str | None = None,
    ) -> UserDomain:

        user_obj = UserDomain(
            email=email,
            hashed_password=hashed_password,
        )
        new_user = self._user_repository.add(user_obj)

        return new_user

    def start(
        self,
        email: str,
        phone: str | None = None,
    ) -> RegistrationStartingResult:
        """
        #TODO
        For now local development i am sending mail directly later
        i will need to switch to celery and say the user that otp has send.

        It need to send otp in background and send response to user
        quickly i will do this later

        Raise:
            InvalidEmailError
        """
        # This email checking is like business logic if email domain is allowed
        # not spammed domain is allowed here liekt his
        try:
            validated_email_id = ValidatedEmail(
                email_id=email,
            ).value
        except InvalidEmailError:
            # my routes can handle this error there and say user
            raise

        #  i am passing this object so that my routes can decide to do with this
        identity_obj = RegistrationIdentity(
            email=validated_email_id,
            phone=phone,
        )

        existing_user = self._user_repository.get_by_email(
            email=validated_email_id,
        )

        if existing_user:

            if existing_user.hashed_password:
                x = RegistrationStartingResult(
                    status=RegistrationStatus.EMAIL_ALREADY_REGISTERED,
                    next_step=AfterRegistrationNextStep.LOGIN_WITH_PASSWORD,
                    identity=identity_obj,
                )
                return x

            else:
                x = RegistrationStartingResult(
                    status=RegistrationStatus.EMAIL_ALREADY_REGISTERED,
                    next_step=AfterRegistrationNextStep.LOGIN_WITH_OTP,
                    identity=identity_obj,
                )
                return x

        otp_send = send_otp_to_email(
            email_id=validated_email_id,
            purpose=OTPPurpose.REGISTER,
        )

        # Below the data from the otp backend is converted to shows
        # in the interface layer of how to do shows the data

        if otp_send.success:
            x = RegistrationStartingResult(
                status=RegistrationStatus.OTP_SENT,
                next_step=AfterRegistrationNextStep.VERIFY_OTP,
                identity=identity_obj,
            )
            return x

        elif otp_send.status == OTPSendStatus.COOLDOWN_ACTIVE:
            return RegistrationStartingResult(
                status=RegistrationStatus.OTP_COOLDOWN_ACTIVE,
                next_step=AfterRegistrationNextStep.SHOW_ERROR,
                identity=identity_obj,
            )

        elif otp_send.status == OTPSendStatus.EMAIL_BLOCKED:
            return RegistrationStartingResult(
                status=RegistrationStatus.EMAIL_BLOCKED,
                next_step=AfterRegistrationNextStep.SHOW_ERROR,
                identity=identity_obj,
            )

        elif otp_send.status == OTPSendStatus.ATTEMPT_LIMIT_EXCEEDED:
            return RegistrationStartingResult(
                status=RegistrationStatus.ATTEMPT_LIMIT_EXCEED,
                next_step=AfterRegistrationNextStep.SHOW_ERROR,
                identity=identity_obj,
            )

        elif otp_send.status in (
            OTPSendStatus.SEND_FAILED,
            OTPSendStatus.EMAIL_SERVER_FAILED,
        ):
            return RegistrationStartingResult(
                status=RegistrationStatus.EMAIL_SERVICE_FAILED,
                next_step=AfterRegistrationNextStep.SHOW_ERROR,
                identity=identity_obj,
            )

        else:
            x = RegistrationStartingResult(
                status=RegistrationStatus.EMAIL_SERVICE_FAILED,
                next_step=AfterRegistrationNextStep.SHOW_ERROR,
                identity=identity_obj,
            )

            return x

    def email_otp_verify(
        self,
        email: str,
        submitted_otp: str,
    ) -> RegistrationViaOTPResult:
        """
        For success it will insert data into the db
        and then if wrong any then it will raise a error

        Raise:
            InvalidEmailError

        """
        # even though i think this checkin is not need here, as the email in session should
        # has been validated beforehand
        try:
            validated_email_id = ValidatedEmail(
                email_id=email,
            ).value
        except InvalidEmailError:
            raise

        verify = verify_otp_against_email(
            email=validated_email_id,
            purpose=OTPPurpose.REGISTER,
            submitted_otp=submitted_otp,
        )

        match verify.status:
            case OTPVerifyStatus.VERIFIED:
                new_user = self._add_user_to_db(
                    email=validated_email_id,
                )
                return RegistrationViaOTPResult(
                    status=RegistrationOTPStatus.VERIFIED,
                    user=new_user,
                )

            case OTPVerifyStatus.INVALID_OTP:
                return RegistrationViaOTPResult(
                    status=RegistrationOTPStatus.INVALID_OTP,
                )

            case OTPVerifyStatus.OTP_NOT_FOUND:
                return RegistrationViaOTPResult(
                    status=RegistrationOTPStatus.OTP_NOT_FOUND,
                )

            case OTPVerifyStatus.ATTEMPT_LIMIT_EXCEEDED:
                return RegistrationViaOTPResult(
                    status=RegistrationOTPStatus.ATTEMPT_LIMIT_EXCEEDED,
                )

    def resend_otp(
        self,
        email: str,
        phone: str | None = None,
    ) -> RegistrationStartingResult:
        """
        i will need to impliment the phone number later
        """
        obj = self.start(
            email=email,
            phone=phone,
        )
        return obj

        # try:
        #     validated_email = ValidatedEmail(
        #         email_id=email,
        #     ).value
        # except InvalidEmailError:
        #     raise

        # otp_send = send_otp_to_email(
        #     email_id=validated_email,
        #     purpose=OTPPurpose.REGISTER,
        # )

        # if otp_send.success:
        #     return RegistrationStartingResult(
        #         status=RegistrationStatus.OTP_SENT,
        #         next_step=AfterRegistrationNextStep.VERIFY_OTP,
        #     )

        # if otp_send.status == OTPSendStatus.COOLDOWN_ACTIVE:
        #     return RegistrationStartingResult(
        #         status=RegistrationStatus.OTP_COOLDOWN_ACTIVE,
        #         next_step=AfterRegistrationNextStep.SHOW_ERROR,
        #     )

        # if otp_send.status == OTPSendStatus.ATTEMPT_LIMIT_EXCEEDED:
        #     return RegistrationStartingResult(
        #         status=RegistrationStatus.ATTEMPT_LIMIT_EXCEED,
        #         next_step=AfterRegistrationNextStep.SHOW_ERROR,
        #     )

        # return RegistrationStartingResult(
        #     status=RegistrationStatus.EMAIL_SERVICE_FAILED,
        #     next_step=AfterRegistrationNextStep.SHOW_ERROR,
        # )

    def set_password(
        self,
        user_id: str,
        password: str,
    ) -> UserDomain | None:
        user = self._user_repository.get_by_id(
            user_id=user_id,
        )
        if user is None:
            return None

        hashed_password = self._password_hasher.make_hash(
            password=password,
        )

        user.hashed_password = hashed_password

        self._user_repository.update_password(
            user=user,
            hashed_password=hashed_password,
        )
        return user
