"""
app/features/identity/infrastructure/sqlmodel/mapper.py

This is for convert my models to business need like this
"""

from ...domain.entities.user import UserDomain

from .models import UserModel


def to_domain(
    model_obj: UserModel,
) -> UserDomain:
    """
    from the sqlmodel database user to my business entities
    userclass i will make here
    """

    full_name = (
        " ".join(name for name in (model_obj.first_name, model_obj.last_name) if name)
        or None
    )

    obj = UserDomain(
        id_=model_obj.id_,
        email=model_obj.email,
        full_name=full_name,
        hashed_password=model_obj.hashed_password,
        is_active=model_obj.is_active,
        is_verified=model_obj.is_verified,
    )

    return obj


def to_model(
    user_obj: UserDomain,
) -> UserModel:
    """
    get the entity user obj and make this to be in sqlmodle table
    data to use
    The userdomain which comes to me there id_ = None as i think for registration
    """
    if user_obj.id_ is None:
        return UserModel(
            email=user_obj.email,
            hashed_password=user_obj.hashed_password,
            is_active=user_obj.is_active,
            is_verified=user_obj.is_verified,
        )

    else:
        obj = UserModel.model_validate(
            user_obj,
        )
        return obj
