"""
app/shared/mail/infrastructure/sender.py

Here i will make the real implimentations of how to send the
mails
"""

from email.message import EmailMessage

import smtplib
import ssl


from pydantic import EmailStr


from ..email_builder import build_email_message
from ..exceptions import EmailSendError
from ..interfaces.sender import EmailSender
from ..models import SMTPConfig, EmailMessageData, AuthSMTPConfig


class LocalMailSender(EmailSender):
    def __init__(
        self,
        mail_config: SMTPConfig,
        default_from: EmailStr,
    ) -> None:
        self.config = mail_config
        self.default_from = default_from

    def send_mail(
        self,
        email_msg: EmailMessageData,
    ) -> None:
        msg = build_email_message(
            email_msg=email_msg,
            default_from_email=self.default_from,
        )
        with smtplib.SMTP(
            host=self.config.host,
            port=self.config.port,
        ) as server:
            server.send_message(
                msg=msg,
            )


class SMTPMailSender(EmailSender):

    def __init__(
        self,
        mail_config: AuthSMTPConfig,
        default_from: EmailStr,
    ) -> None:
        self.config = mail_config
        self.default_from = default_from

    def _send_over_ssl(
        self,
        context: ssl.SSLContext,
        msg: EmailMessage,
    ) -> None:
        with smtplib.SMTP_SSL(
            host=self.config.host,
            port=self.config.port,
            context=context,
        ) as server:
            server.login(
                user=self.config.username,
                password=self.config.password,
            )
            server.send_message(
                msg=msg,
            )

    def _send_over_starttls(
        self,
        context: ssl.SSLContext,
        msg: EmailMessage,
    ) -> None:

        with smtplib.SMTP(
            host=self.config.host,
            port=self.config.port,
        ) as server:
            server.ehlo()
            server.starttls(
                context=context,
            )
            server.ehlo()
            server.login(
                user=self.config.username,
                password=self.config.password,
            )
            server.send_message(
                msg=msg,
            )

    def send_mail(
        self,
        email_msg: EmailMessageData,
    ) -> None:
        msg = build_email_message(
            email_msg=email_msg,
            default_from_email=self.default_from,
        )
        context = ssl.create_default_context()

        try:

            if self.config.security == "ssl":
                self._send_over_ssl(
                    context=context,
                    msg=msg,
                )
            elif self.config.security == "starttls":
                self._send_over_starttls(
                    context=context,
                    msg=msg,
                )

            else:
                raise ValueError(
                    f"Unsupported SMTP Security Mode: {self.config.security}",
                )

        except smtplib.SMTPException as e:
            raise EmailSendError(
                f"SMTP error: {e}",
            ) from e

        except (OSError, TimeoutError) as e:
            raise EmailSendError(
                f"SMTP connection error: {e}",
            ) from e

        except Exception as e:
            raise EmailSendError(
                f"Unexpected email error: {e}",
            ) from e
