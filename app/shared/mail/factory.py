"""
app/shared/mail/factory.py

This will make my email service of what to use in my all
the places, it will create the service properly here which i will use
to send mail to other user.
"""

from app.config import settings
from .config import local_config, email_config
from .interfaces.sender import EmailSender
from .infrastructure.sender import LocalMailSender, SMTPMailSender


def get_mail_sender() -> EmailSender:
    """
    It will return what mail sender my app will use
    """
    if settings.mail.provider == "local":
        s = LocalMailSender(
            mail_config=local_config,
            default_from=settings.mail.address.from_email_default,
        )
        return s

    elif settings.mail.provider == "smtp":
        s = SMTPMailSender(
            mail_config=email_config,
            default_from=settings.mail.address.from_email_default,
        )
        return s
    else:
        raise ValueError("EmailSender Not Created Successfully.")


mail_sender_obj = get_mail_sender()
