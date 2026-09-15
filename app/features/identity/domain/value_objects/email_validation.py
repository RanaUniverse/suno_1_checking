"""
app/features/identity/domain/email_validation.py

Here my email validaion will logic stays so that my service dont
know how the validiaon works and which way?
"""

from pydantic import EmailStr, ValidationError, BaseModel, field_validator


from ..exceptions import InvalidEmailError


class EmailModel(BaseModel):
    value: EmailStr

    @field_validator("value")
    @classmethod
    def allowed_providers(cls, email: EmailStr):
        # later this will come from configuration #TODO
        # i will later say to come this domains from the env variables or db
        allowed_domains = {
            "gmail.com",
            "hotmail.com",
            "outlook.com",
            "yahoo.com",
        }

        domain = str(email).split("@")[-1].lower()

        if domain not in allowed_domains:
            raise InvalidEmailError(
                "Only Trusted Gmail, Hotmail, Outlook, and Yahoo emails are allowed. Else Contact Support."
            )

        return email


class ValidatedEmail:
    """

    Raise
    InvalidEmailError from exceptions.py
    """

    def __init__(
        self,
        email_id: str,
    ) -> None:
        try:
            # below model will check my mail domain to allow or not
            model = EmailModel(
                value=email_id,
            )

        except InvalidEmailError:
            # this exception can raised because of the EmailModel class can do this
            raise

        except ValidationError:
            raise InvalidEmailError(
                "Please Use Your Proper Email ID",
            )
        self._value = str(model.value).lower()

    @property
    def value(self) -> EmailStr:
        email_str = self._value
        return email_str
