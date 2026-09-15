"""
app/shared/mail/interfaces/sender.py

"""

from typing import Protocol


from ..models import EmailMessageData


class EmailSender(Protocol):
    """
    This is the interface class all others class which seems to be email sender
    must be have these methods i write in this class
    1. send_mail()
    """

    def send_mail(
        self,
        email_msg: EmailMessageData,
    ) -> None:
        pass
