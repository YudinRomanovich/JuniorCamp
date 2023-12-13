from sqlalchemy import Column, Integer, String, Table
from sqlalchemy.orm import Mapped
from database import metadata, Base


project = Table(
    "project",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String, nullable=False),
    Column("description", String, nullable=False),
    Column("author_id", Integer, nullable=False),
    Column("needed_skills", String),
)


class ProjectCreate(Base):
    __tablename__ = "project_create"

    id: Mapped[int] = Column(Integer, primary_key=True)
    name: Mapped[str] = Column(String, nullable=False)
    description: Mapped[str] = Column(String, nullable=False)
    author_id: Mapped[int] = Column(Integer, nullable=False)
    needed_skills: Mapped[str] = Column(String)