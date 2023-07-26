from sqlalchemy import Column, String, Text

from app.core.db import Base


class CharityProject(Base):
    name = Column(String, unique=True)
    description = Column(Text)
