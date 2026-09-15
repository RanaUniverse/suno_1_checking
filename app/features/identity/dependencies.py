"""
app/features/identity/dependencies.py


Composition root / dependency wiring for the identity feature.

This module connects:

    Presentation
        ↓
    Application services
        ↓
    Domain abstractions
        ↓
    Infrastructure implementations

The application/domain layers don't know which persistence
technology is being used.

These are keeping dependencies roviders/factories
This module contains dependency providers and application
wiring for the identity feature.
"""

from typing import Annotated


from flask_di import Depends


from app.config import settings

from .domain.repositories.user_repository import UserRepository

from .application.registration.service import RegistrationService
from .application.login.service import LoginService

from .infrastructure.sqlmodel.user_repository import SQLModelUserRepository
from .infrastructure.in_memory.user_repository import InMemoryUserRepository
from .infrastructure.mongo.user_repository import MongoDBUserRepository

from .infrastructure.security.bcrypt_password_hasher import BcryptPasswordHasher

from app.database.session import SessionDep

# ============================================================
# Infrastructure providers
# ============================================================


def get_sqlmodel_repository(
    session: SessionDep,
) -> UserRepository:
    """
    make the SQLModel implementation of UserRepository.

    The Session comes from get_session().
    """

    return SQLModelUserRepository(
        session=session,
    )


def get_mongo_repository() -> UserRepository:

    return MongoDBUserRepository()


def get_memory_repository() -> UserRepository:

    return InMemoryUserRepository()


# ============================================================
# Select the implementation at application startup
# ============================================================

login_provier_value = settings.app.login_backend

if login_provier_value == "SQLMODEL":
    user_repository_provider = get_sqlmodel_repository

elif login_provier_value == "MONGODB":
    raise RuntimeError(
        "MongoDb has not setup yet for login backend pls choose another",
    )
    user_repository_provider = get_mongo_repository

elif login_provier_value == "MEMORY":
    user_repository_provider = get_memory_repository

else:
    raise RuntimeError(
        f"Unknown login backend: {settings.app.login_backend}",
    )


UserRepositoryDep = Annotated[
    UserRepository,
    Depends(
        user_repository_provider,
    ),
]


def get_registration_service(
    user_repository: UserRepositoryDep,
) -> RegistrationService:
    """
    i need to call this fun as a Depends() function
    """

    return RegistrationService(
        user_repository=user_repository,
        password_hasher=BcryptPasswordHasher(),
    )


def get_login_service(
    user_repository: UserRepositoryDep,
) -> LoginService:
    """
    I need to call this aas a Depends() function
    """
    return LoginService(
        user_repository=user_repository,
        password_hasher=BcryptPasswordHasher(),
    )


# i will call this below in the routes.py' function
RegistrationServiceDep = Annotated[
    RegistrationService,
    Depends(
        get_registration_service,
    ),
]


LoginServiceDep = Annotated[
    LoginService,
    Depends(
        get_login_service,
    ),
]
