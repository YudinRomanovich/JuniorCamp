
from datetime import datetime

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import LargeBinary, Table, Boolean, Column, Integer, String, TIMESTAMP

from database import metadata, Base

user = Table(
    "user",
    metadata,
    Column("skills", String),
    Column("profession", String),
    Column("id", Integer, primary_key=True),
    Column("username", String, nullable=False, unique=True),
    Column("hashed_password", String, nullable=False),
    Column("registered_at", TIMESTAMP, default=datetime.utcnow),
    Column("email", String(length=320), unique=True, index=True, nullable=False),
    Column("is_active", Boolean, default=True, nullable=False),
    Column("is_superuser", Boolean, default=False, nullable=False),
    Column("is_verified", Boolean, default=False, nullable=False),
    Column("profile_image", LargeBinary)
)

class User(SQLAlchemyBaseUserTable[int], Base):
    registered_at = Column(TIMESTAMP, default=datetime.utcnow)
    id = Column(Integer, primary_key=True) 
    username = Column(String, nullable=False)
    email: str = Column(String(length=320), unique=True, index=True, nullable=False)
    skills: str = Column(String)
    profession: str = Column(String)
    hashed_password: str = Column(String(length=1024), nullable=False)
    is_active: bool = Column(Boolean, default=True, nullable=False)
    is_superuser: bool = Column(Boolean, default=False, nullable=False)
    is_verified: bool = Column(Boolean, default=False, nullable=False)
    profile_image: bytes = Column(LargeBinary)

