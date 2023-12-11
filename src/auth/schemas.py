from typing import Optional

from fastapi_users import schemas


class UserRead(schemas.BaseUser[int]):
    id: int
    username: str
    email: str
    skills: str
    profession: str
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False
    profile_image: bytes = None
    
    class Config:
        orm_mode = True


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
    profile_image: Optional[bytes] = None
