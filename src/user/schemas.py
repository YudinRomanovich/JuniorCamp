from typing import Optional
from fastapi_users import schemas
from pydantic import ConfigDict


class UserRead(schemas.BaseUser[int]):
    model_config = ConfigDict()

    id: int
    username: str
    email: str
    skills: str
    profession: str
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False
    
    # class Config:
    #     from_attributes = True


class UserCreate(schemas.BaseUserCreate):
    id: int
    username: str
    email: str
    password: str
    skills: str
    profession: str
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    is_verified: Optional[bool] = False