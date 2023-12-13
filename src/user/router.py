from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import delete, select, update
from auth.base_config import current_user
from user.models import user
from database import get_async_session


router = APIRouter(
    prefix="",
    tags=["User"]
)


@router.delete('/delete')
async def delete_current_user(
    session: AsyncSession = Depends(get_async_session),
    session_user=Depends(current_user)
):
    try:
        
        stmt = (
            delete(user)
            .where(user.c.username == session_user.username)
        )
        
        await session.execute(stmt)
        await session.commit()
        return {
            "status" : 200
        }

    except:
        raise HTTPException(status_code=500, detail={
                "status": "error",
                "data": None,
                "detail": None
            })
    

@router.put('/edit')
async def edit_current_user(
    new_username: str,
    new_profession: str,
    new_skills: str,
    session: AsyncSession = Depends(get_async_session),
    session_user=Depends(current_user)
):
    try:
        stmt = (
            update(user)
            .where(user.c.username == session_user.username)
            .values(
                username=new_username,
                profession=new_profession,
                skills=new_skills
            )
        )
        await session.execute(stmt)
    
        await session.commit()
        return {
            "status" : 200
        }

    except:
        raise HTTPException(status_code=500, detail={
                "status": "error",
                "data": None,
                "detail": None
            })
    

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