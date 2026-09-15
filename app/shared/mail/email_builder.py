"""
app/shared/mail/email_builder.py

This will make the email content here and i will pass this
in my sender or others so that it will use easily
"""

from email.message import EmailMessage


from pydantic import EmailStr


from .models import EmailMessageData


def build_email_message(
    email_msg: EmailMessageData,
    default_from_email: EmailStr,
) -> EmailMessage:
    """
    Here i will pass my pydantic class
    and it will make this python inbuild EmailMessage
    so that i can use this in server.send_message

    The email sender will call this before sending a mail
    """
    msg = EmailMessage()
    msg["From"] = str(email_msg.from_email or default_from_email)
    msg["To"] = email_msg.to_email
    msg["Subject"] = email_msg.subject
    msg.set_content(email_msg.body_text)

    if email_msg.body_html:
        msg.add_alternative(
            email_msg.body_html,
            subtype="html",
        )
    if email_msg.cc:
        msg["Cc"] = email_msg.cc
    if email_msg.bcc:
        msg["Bcc"] = email_msg.bcc
    if email_msg.reply_to:
        msg["Reply-To"] = email_msg.reply_to

    return msg
