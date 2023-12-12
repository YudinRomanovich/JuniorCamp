from fastapi import APIRouter, Depends, HTTPException
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from auth.models import User, user
from database import get_async_session

router = APIRouter(
    prefix="",
    tags=["User"]
)


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)

@router.get('/get')
async def get_specific_user(
    username: str,
    session: AsyncSession = Depends(get_async_session)
):
    try:
        query = select(user).where(user.c.username == username)
        result = await session.execute(query)
        dict_user = []
        for item in result.all():
            dict_user.append({
                "username": item[3],
                "profession": item[1],
                "skills": item[0],
                "email": item[6],
            })
        return {
            "status": "success",
            "data": dict_user,
            "detail": None
        }
    except:
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": None,
            "detail": None
        })
