"""
app/shared/otp/models.py

I will use this for models to reprreset the data
and then i will use this for send or use
"""

from pydantic import BaseModel, Field


from .enums import OTPSendStatus, OTPVerifyStatus


class OTPSendResult(BaseModel):
    """
    After the backend try to send the opt
    it will send this result class
    """

    status: OTPSendStatus
    message: str

    @property
    def success(
        self,
    ):
        r = self.status == OTPSendStatus.SENT
        return r


class OTPVerifyResult(BaseModel):
    """
    After i try to verify otp is validated or not
    this should to return to the user interface
    """

    status: OTPVerifyStatus
    message: str | None = None

    @property
    def success(self) -> bool:
        r = self.status == OTPVerifyStatus.VERIFIED
        return r


class OTPPolicy(
    BaseModel,
    frozen=True,
):
    """
    On OTP Send time i will use validity, cooldown, length.
    And Verification time i will use: max_attempts.
    """

    validity: int = Field(
        description="How many second the otp will validity",
        gt=0,
    )

    cooldown: int = Field(
        description="For how many second the otp resend will be stop",
        gt=0,
    )

    max_attempts: int = Field(
        gt=0,
        description="Maxximum Number of verificaiton attempst",
    )

    length: int = Field(
        description="The Lenght of the otp whcih will be stored or generate "
        "for differnet reasons based on otppurpose",
        gt=0,
        lt=100,
    )


class OTPEmailPresentation(BaseModel, frozen=True):
    """
    This is represents the email structer file to shows
    """

    subject_template: str
    text_template: str
    html_template: str


class RenderedOTPEmail(BaseModel, frozen=True):
    """
    This will have the information of the final email data
    """

    subject: str
    body_text: str
    body_html: str
