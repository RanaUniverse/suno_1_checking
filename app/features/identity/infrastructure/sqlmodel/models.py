"""
app/features/identity/infrastructure/sqlmodel/models.py

The actual database table. SQLModel only. This file must NEVER be
imported by domain/ or application/ — only infrastructure/ touches it.


For Password to hash_password i will use one function
and then i will use this in a extra_data and use update=extra_data in model_validate

https://sqlmodel.tiangolo.com/tutorial/fastapi/update-extra-data/#create-a-model-object-with-extra-data

"""

from datetime import datetime


from sqlmodel import SQLModel, Field


from app.shared.utils import generate_hex_uuid4


class UserBase(SQLModel):
    """
    This will be the base model for most of other to inherit from
    """

    first_name: str | None = Field(
        default=None,
        description="This is the First name of user given by user after registraion"
        "if he wants to give his name",
    )

    last_name: str | None = Field(
        default=None,
        description="Last name of the user maybe not given by user will ok ",
    )

    email: str = Field(
        unique=True,
        index=True,
    )

    last_login_time: datetime | None = None

    is_active: bool = True

    is_verified: bool = False


class UserCreate(UserBase):
    password: str


class UserModel(
    UserBase,
    table=True,
):
    id_: str = Field(
        default_factory=generate_hex_uuid4,
        primary_key=True,
    )

    hashed_password: str | None = Field(
        default=None,
        description="From the password i will make the hashed_password"
        " or not deciding if user has password or not",
    )


class UserPublic(UserBase):
    """
    For now i dont need it maybe i will use for api things
    """

    id_: str


class UserUpdate(SQLModel):

    first_name: str | None
    last_name: str | None
    email: str | None
    is_active: bool | None = None
    is_verified: bool | None = None
    password: str | None = None
