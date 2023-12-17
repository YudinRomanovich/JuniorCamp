from pydantic import BaseModel


class FriendCreate(BaseModel):
    id: int
    user_id: int
    list_of_friends: list

    class Config:
        from_attributes = True


class FriendRead(BaseModel):
    id: int
    user_id: int
    list_of_friends: list