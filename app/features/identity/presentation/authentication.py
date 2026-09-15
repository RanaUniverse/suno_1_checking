"""
app/features/identity/presentation/authentication.py

Here i will write my user class for flask_login related thigns
"""

from flask_di import (
    Depends,
    current_app,
)

from flask_login import (  # type: ignore
    UserMixin,
)

from ..domain.entities.user import UserDomain


from ..dependencies import user_repository_provider

from app.shared.extensions import login_manager


class FlaskLoginUser(UserMixin):
    """
    This present the user class need by flask_login to have here
    """

    def __init__(
        self,
        user: UserDomain,
    ) -> None:
        self._user = user

    def get_id(self):
        """
        I make this as per the docs of the flask_login i need to have a way
        to return the str to uniquely represent a user so that it will
        save in the cookie and later i can get user obj from this

        https://flask-login.readthedocs.io/en/latest/#your-user-class
        """
        unique_id_represent_the_user = self._user.id_
        return str(unique_id_represent_the_user)

    @property
    def domain_user(self) -> UserDomain:
        return self._user


@login_manager.user_loader  # type: ignore
def load_user(
    user_id: str,
) -> FlaskLoginUser | None:
    """
    https://flask-login.readthedocs.io/en/latest/#how-it-works
    As per the docs it should return the obj or the None.

    This will read the user_id from the cookie and convert into the user obj
    from the user_obj i will get differnt data to use.
    """

    user_repository = current_app.resolve(
        Depends(
            user_repository_provider,
        )
    )

    obj_domain = user_repository.get_by_id(
        user_id,
    )

    if obj_domain is None:
        return None

    obj = FlaskLoginUser(
        obj_domain,
    )

    return obj
