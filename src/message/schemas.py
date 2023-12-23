from pydantic import BaseModel
from sqlalchemy import TIMESTAMP


class MassageCreate(BaseModel):
    user_id: int
    from_id: int
    to_id: int
    massages: list
    date: TIMESTAMP

    class Config:
        from_attributes = True


class MassageRead(BaseModel):
    user_id: int
    from_id: int
    to_id: int
    massages: list
    date: TIMESTAMP