from sqlalchemy import ARRAY, Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import Mapped, relationship
from database import metadata, Base
from user.models import User


friend = Table(
    "friend",
    metadata,
    Column("id", Integer, primary_key=True , unique=True),
    Column("user_id", Integer, ForeignKey('user.id'), unique=True),
    Column("list_of_friends", ARRAY(Integer), default=None, nullable=True)
)


class Friend(Base):
    __tablename__ = "friend"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    list_of_friends = Column(ARRAY(Integer), default=[], nullable=False)
    user = relationship("User")

