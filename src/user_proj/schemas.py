from pydantic import BaseModel

class UserProject(BaseModel):
    user_id: int
    project_id: int

    class Config:
        orm_mode = True
