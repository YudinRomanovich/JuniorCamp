from sqlalchemy import Column, ForeignKey, Integer, Table
from sqlalchemy.orm import Mapped
from database import metadata, Base


user_project = Table(
    "user_project",
    metadata,
    Column("user_id", Integer, ForeignKey("user.id"), primary_key=True),
    Column("project_id", Integer, ForeignKey("project.id"), primary_key=True)
)

class UserProject(Base):
    __tablename__ = "user_project"

    user_id: Mapped[int] = Column(Integer, ForeignKey("user.id"), primary_key=True)
    project_id: Mapped[int] = Column(Integer, ForeignKey("project.id"), primary_key=True)
