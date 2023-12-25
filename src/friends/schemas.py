from pydantic import BaseModel, ConfigDict


class FriendCreate(BaseModel):

    model_config = ConfigDict()

    id: int
    user_id: int
    list_of_friends: list

    # class Config:
    #     from_attributes = True


class FriendRead(BaseModel):
    id: int
    user_id: int
    list_of_friends: list