from fastapi import Depends, HTTPException
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from auth.models import User, user
from database import get_async_session


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)

async def get_specific_user(
    username: str,
    session: AsyncSession = Depends(get_async_session)
):
    try:
        query = select(user).where(user.c.username == username)
        result = await session.execute(query)
        return {
            "status": "success",
            "data": result.first(),
            "detail": None
        }
    except:
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": None,
            "detail": None
        })
