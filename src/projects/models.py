from sqlalchemy import Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship, Mapped

from database import metadata, Base


project = Table(
    "project",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String),
    Column("description", String),
    Column("author_id", Integer, ForeignKey("user.id")),
    Column("needed_skills", String),
)

class ProjectCreate(Base):
    __tablename__ = "project_create"

    id: Mapped[int] = Column(Integer, primary_key=True)
    name: Mapped[str] = Column(String)
    description: Mapped[str] = Column(String)
    author_id: Mapped[int] = Column(Integer, ForeignKey("user.id"))

    author = relationship("User", back_populates="project")
    p_members = relationship("User", secondary="user_project")
    needed_skills: Mapped[str] = Column(String)
