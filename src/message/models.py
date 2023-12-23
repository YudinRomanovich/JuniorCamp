from datetime import datetime
from sqlalchemy import TIMESTAMP, Column, Integer, String, Table
from sqlalchemy.orm import Mapped
from database import Base, metadata


message = Table(
    "message",
    metadata,
    Column("message_id", Integer, primary_key=True, nullable=False, unique=True),
    Column("from_id", Integer, nullable=False),
    Column("to_id", Integer, nullable=False),
    Column("message", String, nullable=True, default=None),
    Column("date", TIMESTAMP, default=datetime.utcnow)
)


class Message(Base):
    __tablename__ = "message"

    message_id: Mapped[int] = Column(nullable=False, primary_key=True, unique=True)
    from_id: Mapped[int] = Column(nullable=False)
    to_id: Mapped[int] = Column(nullable=False)
    massage: Mapped[str] = Column(nullable=True, default=None)
    date: Mapped[TIMESTAMP] = Column(default=datetime.utcnow)