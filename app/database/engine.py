"""
app/database/engine.py

Here i will defines the engine
"""

from sqlmodel import create_engine


from ..config import settings

engine = create_engine(
    url=settings.db.db_url,
)
