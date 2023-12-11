from pydantic import BaseModel

class ProjectCreate(BaseModel):
    id: int
    name: str
    description: str
    author_id: int
    needed_skills: str

    class Config:
        orm_mode = True

class ProjectRead(BaseModel):
    id: int
    name: str
    description: str
    author_id: int
    needed_skills: str