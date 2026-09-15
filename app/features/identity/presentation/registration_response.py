"""
app/features/identity/presentation/registration_response.py

Here i will decide  what to do based on the registion result of next step
This is related to the routes.py
"""

from flask import (
    redirect,
    url_for,
    flash,
)


from ..application.registration.dto import RegistrationStartingResult
from ..domain.enums import AfterRegistrationNextStep

from app.shared.frontend.enums import FlashCategory
from app.shared.session.enums import IdentitySessionKey
from app.shared.session.service import set_identity_key as set_identity_key_in_session
from .message import registration_to_flash

# def get_required_email(
#     result: RegistrationResult,
# ) -> str | None:
#     """
#     From the registration result it will give me his email
#     """

#     if result.identity is None:
#         return None

#     return result.identity.email


# def get_registration_identity(
#     result: RegistrationResult,
# ) -> RegistrationIdentity | None:
#     return result.identity


def handle_registration_result(
    result: RegistrationStartingResult,
):
    """
    This fun is like the same level of the routes.py function
    This will just a extension not to write in the fun but keep here
    """

    information = registration_to_flash(
        result=result,
    )

    flash(
        message=information.message,
        category=information.category,
    )
    # later i will think how i can add phone, email or somethig username
    identity = result.identity

    if identity is None:
        # i wish this will not happens
        flash(
            message="Somethign is wron ghere, ",
            category=FlashCategory.WARNING,
        )
        return redirect(url_for("auth_bp.register"))

    match result.next_step:

        case AfterRegistrationNextStep.VERIFY_OTP:

            set_identity_key_in_session(
                key=IdentitySessionKey.REGISTER_PENDING,
                email_value=identity.email,
                phone_value=identity.phone,
            )

            return redirect(
                url_for(
                    "auth_bp.verify_registration_otp",
                )
            )

        case AfterRegistrationNextStep.LOGIN_WITH_PASSWORD:
            set_identity_key_in_session(
                key=IdentitySessionKey.LOGIN_PENDING,
                email_value=identity.email,
                phone_value=identity.phone,
            )
            # later in time of login with password i need check phone number
            return redirect(
                url_for(
                    "auth_bp.login",
                )
            )

        case AfterRegistrationNextStep.LOGIN_WITH_OTP:
            set_identity_key_in_session(
                key=IdentitySessionKey.LOGIN_PENDING,
                email_value=identity.email,
                phone_value=identity.phone,
            )
            # later in time of login with password i need check phone number
            flash(
                message=f"You Have Not Any Password You Must Need to use OTP Login",
                category=FlashCategory.SECONDARY,
            )
            return redirect(
                url_for(
                    "auth_bp.login_with_otp",
                )
            )

        case AfterRegistrationNextStep.SHOW_ERROR:

            return redirect(
                url_for(
                    "auth_bp.register",
                )
            )

        case _:
            # i will do some check here later
            flash(
                "Somethign went wrong pls report to admin",
                "warning",
            )
            return redirect(
                url_for(
                    "auth_bp.register",
                )
            )
