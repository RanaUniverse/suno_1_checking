"""
app/features/identity/forms.py

Here i will defines the class for my flask_wtf forms
"""

from flask_wtf import (  # type: ignore
    FlaskForm,
)

from wtforms import (
    PasswordField,
    SubmitField,
    StringField,
    EmailField,
)

from wtforms.validators import (
    DataRequired,
    Length,
    Email,
    Optional,
    # EqualTo,
)


class PhoneNumberMixin:
    phone = StringField(
        label="Phone Number(Optional)",
        validators=[
            Optional(),
            Length(
                min=10,
                max=10,
                message="Phone Number Must Be %(min)d Digits",
            ),
        ],
        render_kw={
            "autocomplete": "tel",
            "inputmode": "tel",
        },
    )


class EmailMixin:
    email = EmailField(
        label="Email ID",
        validators=[
            DataRequired(),
            Length(
                min=1,
                max=50,
            ),
            Email(),
        ],
    )
    # i use below sometime to check if frontend fails to email id check i will
    # check with below valud if my backend will do it properly

    # email = StringField(
    #     label="Email ID",
    #     validators=[
    #         DataRequired(),
    #         Length(
    #             min=1,
    #             max=50,
    #         ),
    #     ],
    # )


class LoginForm(FlaskForm, EmailMixin):

    password = PasswordField(
        label="Enter Your Password",
        validators=[
            DataRequired(),
        ],
    )

    submit = SubmitField(
        label="Login Now",
    )


class LoginWithOtpForm(FlaskForm, EmailMixin):
    """
    This will only shows the email id enter form
    """

    submit = SubmitField(label="Send Login OTP")


class RegisterForm(
    FlaskForm,
    EmailMixin,
    PhoneNumberMixin,
):
    submit = SubmitField(
        label="Register New Account",
    )


class OTPForm(FlaskForm):
    """
    I am making the form with init so that i can give dynamically the length value
    """

    otp = StringField(
        label="Enter OTP",
        validators=[
            # Length(
            #     2,
            #     2,
            # ),
            DataRequired(),
        ],
    )
    # i am keeping  DataRequired as the base validator.
    # The OTP length validator is added dynamically in __init__ below in my code.

    submit = SubmitField(
        label="Verify Your OTP",
    )

    def __init__(
        self,
        otp_length: int | None = None,
    ):
        super().__init__()  # type: ignore

        if otp_length is None:
            min_len = 1
            max_len = 10
            label = "Enter Your OTP"

        else:
            min_len = otp_length
            max_len = otp_length
            label = f"Enter {otp_length} digit OTP!"

        # Do not use append() here because we want to avoid mutating
        # the existing validator list between form instances.
        # Create a new list while preserving the existing validators.

        self.otp.validators = [
            *self.otp.validators,
            Length(
                min=min_len,
                max=max_len,
            ),
        ]

        self.otp.render_kw = {
            **(self.otp.render_kw or {}),
            "minlength": str(min_len),
            "maxlength": str(max_len),
        }

        self.otp.label.text = label


class SetPasswordForm(FlaskForm):
    password = PasswordField(
        label="Select A Strong Password",
        validators=[
            DataRequired(),
            Length(
                min=3,
                message="Password must be at least 3 characters long",
            ),
        ],
    )

    # confirm_password = PasswordField(
    #     "Confirm Password",
    #     validators=[
    #         DataRequired(),
    #         EqualTo(
    #             "password",
    #             message="Passwords must match.",
    #         ),
    #     ],
    # )

    submit = SubmitField(
        label="Register Here",
    )
