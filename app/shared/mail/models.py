"""
app/shared/mail/models.py

"""

from typing import Literal


from pydantic import BaseModel, EmailStr, ConfigDict


class SMTPConfig(BaseModel):
    host: str
    port: int


class AuthSMTPConfig(SMTPConfig):
    username: str
    password: str

    security: Literal[
        "ssl",
        "starttls",
    ]


class EmailMessageData(BaseModel):

    model_config = ConfigDict(
        validate_assignment=True,
    )

    to_email: list[EmailStr]

    subject: str
    body_text: str
    body_html: str | None = None

    from_email: EmailStr | None = None
    # if i will not use this upper value it will use from config

    reply_to: EmailStr | None = None
    cc: list[EmailStr] | None = None
    bcc: list[EmailStr] | None = None
