from pydantic import BaseModel, ConfigDict


class ProjectCreate(BaseModel):
    model_config = ConfigDict()

    id: int
    name: str
    description: str
    author_id: int
    needed_skills: str

    # class Config:
    #     from_attributes = True


class ProjectRead(BaseModel):
    id: int
    name: str
    description: str
    author_id: int
    needed_skills: str