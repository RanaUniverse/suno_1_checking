"""
app/database/session.py

Provides SQLModel database sessions.

This module belongs to infrastructure because
Session is a SQLModel/SQLAlchemy implementation detail.

i copy it form the fastapi docs and use the di-flask so it will works

https://sqlmodel.tiangolo.com/tutorial/fastapi/session-with-dependency/

https://github.com/razorblade23/di-flask
"""

from collections.abc import Generator
from typing import Annotated

from sqlmodel import Session

from flask_di import Depends


from app.database.engine import engine


def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session


# TODO i need to confirm using this di-flask will ok
SessionDep = Annotated[
    Session,
    Depends(get_session),
]
