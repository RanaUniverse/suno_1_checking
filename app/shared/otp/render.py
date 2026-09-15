"""
app/shared/otp/render.py

This is responsible to generate the structer of how the mail
data or message will shows to the user.
"""

from flask import render_template


from .domain.enums import OTPPurpose

from .domain.models import OTPEmailPresentation, RenderedOTPEmail

OTP_EMAIL_PRESENTATIONS: dict[OTPPurpose, OTPEmailPresentation] = {
    OTPPurpose.REGISTER: OTPEmailPresentation(
        subject_template="Register Your Account With Our Service",
        text_template="emails/otp/register.txt",
        html_template="emails/otp/register.html",
    ),
    OTPPurpose.LOGIN: OTPEmailPresentation(
        subject_template="Please Login Here With OTP",
        text_template="emails/otp/login.txt",
        html_template="emails/otp/login.html",
    ),
    OTPPurpose.FORGET_PASSWORD: OTPEmailPresentation(
        subject_template="Password Forget Request With OTP",
        text_template="emails/otp/forget_password.txt",
        html_template="emails/otp/forget_password.html",
    ),
}


def render_otp_email(
    *,
    otp: str,
    valid_seconds: int,
    purpose: OTPPurpose,
) -> RenderedOTPEmail:
    """
    Render the text and HTML Version of the otp mail

    purpose -> This value defines which templates are used

    Raise:
        KeyError when the email template not found
    """

    try:
        presentation = OTP_EMAIL_PRESENTATIONS[purpose]

    except KeyError as exc:
        raise RuntimeError(
            f"No email presentation configured for OTP purpose " f"{purpose.value!r}"
        ) from exc

    body_text = render_template(
        template_name_or_list=presentation.text_template,
        otp=otp,
        valid_seconds=valid_seconds,
    )

    body_html = render_template(
        template_name_or_list=presentation.html_template,
        otp=otp,
        valid_seconds=valid_seconds,
    )

    return RenderedOTPEmail(
        subject=presentation.subject_template,
        body_text=body_text,
        body_html=body_html,
    )


def validate_otp_email_presentation() -> None:
    """
    This will validate if i have all the presentation templates
    i make already or not and then based on this i will throw error
    """
    missing = [
        purpose.value
        for purpose in OTPPurpose
        if purpose not in OTP_EMAIL_PRESENTATIONS
    ]
    if missing:
        raise RuntimeError(
            "Missing OTP Email Presentation TEmplates or somethigns", f"{missing}"
        )
