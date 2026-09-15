"""
app/features/identity/infrastructure/sqlmodel/user_repository.py

The implementation:
   "How do I actually query PostgreSQL/SQLite/MongoDB?"

for the sqlmodel i will write code here

"""

# i am using the below class as a protocol to make this below
from ...domain.repositories.user_repository import UserRepository

from ...domain.entities.user import UserDomain
from ....identity.domain.exceptions import MyAppLogicError

# TODO i need to sure if this import is allow or not


from sqlmodel import Session, select

from .mapper import to_domain, to_model
from .models import UserModel


class SQLModelUserRepository(UserRepository):
    """
    I just inherit from the UserRepository just for know what i am doing

    The session will come by the Dependency injection of Depends
    so i will not need to use with context manager.

    These methods actually returns the actual datamodel of entity
    so i need to think and know is this correct for ddd #TODO
    """

    def __init__(
        self,
        session: Session,
    ) -> None:
        self._session = session

        # Now my yield will directly give me the Session so i use this upper from
        # the di-flask's 0.1.8 i checked

        # i have changed upper to below as this library not currently support
        # the yield to return the session so i use below thigns
        # self._session_generator = session
        # self._session_old = next(self._session_generator)
        # self._session = cast(Session, self._session_old)
        # print("Printing session below from yield")
        # print(self._session)

    def get_by_id(
        self,
        user_id: str,
    ) -> UserDomain | None:
        """
        Here user_id is a primary column so i will use the .get()
        """
        obj = self._session.get(
            UserModel,
            user_id,
        )

        if obj is None:
            return None

        return to_domain(obj)

    def get_by_email(self, email: str) -> UserDomain | None:
        """
        Email address is unique so i will use

        as i know this is unique so i use .first() to get first row or none
        """
        statement = select(UserModel).where(
            UserModel.email == email,
        )
        results = self._session.exec(statement)
        obj = results.first()

        if obj is None:
            return None

        return to_domain(obj)

    def exists_by_email(self, email: str) -> bool:
        r = self.get_by_email(email) is None
        return not r

    def add(
        self,
        user: UserDomain,
    ) -> UserDomain:
        """
        Adding the user to the database but the catche is this is coming
        from the userDomain obj i need to convert this
        """
        model_obj = to_model(user)
        self._session.add(model_obj)
        self._session.commit()
        self._session.refresh(model_obj)
        entity_obj = to_domain(model_obj)

        return entity_obj

    def update_password(
        self,
        user: UserDomain,
        hashed_password: str,
    ) -> UserDomain:
        """
        Thsi will take the userid from there and then try to fetch the user
        and then it will update the user details

        Raise:
            MyAppLogicError
        """
        if not user.id_:
            raise MyAppLogicError

        model_obj = self._session.get(
            UserModel,
            user.id_,
        )
        if model_obj is None:
            raise MyAppLogicError
        model_obj.hashed_password = hashed_password

        self._session.add(model_obj)
        self._session.commit()
        self._session.refresh(model_obj)

        return to_domain(
            model_obj=model_obj,
        )
