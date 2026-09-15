"""
app/features/identity/infrastructure/security/bcrypt_password_hasher.py

Here how i will use the password hasing and checking in reality will be her
"""

from app.shared.extensions import flask_bcrypt

from ...domain.services.password_hasher import PasswordHasher


class BcryptPasswordHasher(PasswordHasher):
    def make_hash(
        self,
        password: str,
    ) -> str:
        return flask_bcrypt.generate_password_hash(  # type: ignore
            password=password,
            rounds=10,
        ).decode("utf-8")

    def verify(
        self,
        password: str,
        hashed_password: str,
    ) -> bool:
        return flask_bcrypt.check_password_hash(  # type: ignore
            pw_hash=hashed_password,
            password=password,
        )
