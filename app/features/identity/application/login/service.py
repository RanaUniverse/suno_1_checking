"""
app/features/identity/services.py

Here i will write my business logics like how the login works and so on
"""

from pydantic import EmailStr

from app.shared.otp.domain.enums import OTPPurpose

from ...domain.entities.user import UserDomain
from ...domain.repositories.user_repository import UserRepository
from ...domain.enums import LoginStatus, LoginOTPStatus

from .dto import LoginResult, LoginIdentity, LoginOTPResult

from ...domain.value_objects.email_validation import ValidatedEmail
from ...domain.exceptions import InvalidEmailError

from ..otp.service import send_otp_to_email, verify_otp_against_email
from ...domain.services.password_hasher import PasswordHasher


class LoginService:
    """
    Here i will keep login related thigns so easily i can use those
    """

    def __init__(
        self,
        user_repository: UserRepository,
        password_hasher: PasswordHasher,
    ) -> None:

        self._user_repository = user_repository
        self._password_hasher = password_hasher

    def check_authentication(
        self,
        email: EmailStr,
        password: str,
    ) -> UserDomain | None:
        """
        Authenticate a user using an email address and password.

        Returns:
            User: The authenticated user if the credentials are valid.
            None: If authentication fails.
        """
        obj = self._user_repository.get_by_email(
            email=email,
        )
        if not obj:
            return None

        stored_password_hash = obj.hashed_password
        if stored_password_hash is None:
            # i think this hsould be say user any problme is here
            return None

        # Thsi is coming from the userdomain i think this should be coming
        # from the database directly
        # if password == stored_password_hash:

        if self._password_hasher.verify(
            password=password,
            hashed_password=stored_password_hash,
        ):
            return obj

    def send_otp_for_login(
        self,
        email: str,
    ) -> LoginResult:
        """
        This is the way of sending the otp for login purpose
        """

        try:
            validated_email_id = ValidatedEmail(
                email_id=email,
            ).value
        except InvalidEmailError:
            # my routes can handle this error there and say user
            raise

        identity_obj = LoginIdentity(
            email=validated_email_id,
        )

        existing_user = self._user_repository.get_by_email(
            email=validated_email_id,
        )
        if existing_user is None:
            x = LoginResult(
                status=LoginStatus.NO_ACCOUNT,
            )
            return x
        else:
            # i am calling a fun which call the backend's email send

            otp_send = send_otp_to_email(
                email_id=validated_email_id,
                purpose=OTPPurpose.LOGIN,
            )

            if otp_send.success:
                x = LoginResult(
                    status=LoginStatus.OTP_SENT,
                    identity=identity_obj,
                    full_name=existing_user.full_name,
                )
                return x

            # i need to say him later the reason of failure
            x = LoginResult(
                status=LoginStatus.PROBLEM,
            )
            return x

    def complete_login_with_otp(
        self,
        email: str,
        submitted_otp: str,
    ) -> LoginOTPResult:
        """
        Verify an OTP for an existing user's login.

        The email should come from the pending-login session
        in the route. This service validates the email again,
        verifies the OTP, and returns the existing user only
        when verification succeeds.

        Returns:
            LoginOTPResult:
                VERIFIED -> OTP is valid and user is returned.
                NOT_VERIFIED -> OTP is invalid/expired/etc.
        """
        try:
            validated_email_id = ValidatedEmail(
                email_id=email,
            ).value
        except InvalidEmailError:
            raise

        existing_user = self._user_repository.get_by_email(
            email=validated_email_id,
        )

        if not existing_user:
            return LoginOTPResult(
                status=LoginOTPStatus.NOT_VERIFIED,
            )

        verify = verify_otp_against_email(
            email=validated_email_id,
            purpose=OTPPurpose.LOGIN,
            submitted_otp=submitted_otp,
        )
        if not verify.success:
            return LoginOTPResult(
                status=LoginOTPStatus.NOT_VERIFIED,
            )

        return LoginOTPResult(
            status=LoginOTPStatus.VERIFIED,
            user=existing_user,
        )
