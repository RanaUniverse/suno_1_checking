"""
app/shared/mail/config.py

Here i will make email related conig settings below
which i will use in different places
"""

from app.config import settings

from .models import SMTPConfig, AuthSMTPConfig

local_config = SMTPConfig(
    host="localhost",
    port=1025,
)


# this below values will come from the config
email_config = AuthSMTPConfig(
    host=settings.mail.host,
    port=settings.mail.port,
    username=settings.mail.username,
    password=settings.mail.password.get_secret_value(),
    security=settings.mail.security,
)
