from sqlalchemy import Column, ForeignKey, Integer, Text

from app.core.db import Base


class Donation(Base):
    user_id = Column(Integer, ForeignKey("user.id"))
    comment = Column(Text, nullable=True)
