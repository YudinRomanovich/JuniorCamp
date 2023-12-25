from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import delete, insert, select, and_, update, or_
from sqlalchemy.ext.asyncio import AsyncSession

from user.router import get_specific_user
from auth.base_config import current_user
from message.models import message
from database import get_async_session

router = APIRouter(
    prefix="/messages",
    tags=["Messages"]
)


@router.delete("/delete/{id_message}")
async def delete_message(
    id_message: int,
    user=Depends(current_user),
    session: AsyncSession=Depends(get_async_session)
):
    try:

        check_message = select(message).where(and_(message.c.from_id == user.id, message.c.message_id == id_message))
        res = await session.execute(check_message)
    
        if res.all():
            stmt = delete(message).where(and_(message.c.from_id == user.id, message.c.message_id == id_message))
            await session.execute(stmt)
            await session.commit()
            
            return {
                "status": 200,
                "data": None,
                "detail": "message delete success"
            }
        else:
            return {
                "status": 400,
                "data": None,
                "detail": "you not author of message"

            }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail={
            "status": 500,
            "data": None,
            "detail": str(e)
        })


@router.put("/edit/{id_message}")
async def edit_message(
    id_message: int,
    new_text_message: str,
    user=Depends(current_user),
    session: AsyncSession=Depends(get_async_session)
):
    try:
        check_message = select(message).where(
            and_(message.c.from_id == user.id, message.c.message_id == id_message))
        
        result = await session.execute(check_message)

        one_or_none = result.scalar_one_or_none()

        if one_or_none == None:
            return {
                "status": 400,
                "data": None,
                "detail": "message not exist    "
            }

        stmt = update(message).where(
            and_(message.c.from_id == user.id, message.c.message_id == id_message)).values(
                message=new_text_message
            )
        

        await session.execute(stmt)
        await session.commit()

        return{
            "status": 200,
            "data": None,
            "detail": "message updated"
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail={
            "status": 500,
            "data": None,
            "detail": str(e)
        })


@router.get("/")
async def get_messages(
        session: AsyncSession=Depends(get_async_session),
        user=Depends(current_user)
):
    try:
        stmt = select(message).where(or_(message.c.from_id == user.id, message.c.to_id == user.id))
        res = await session.execute(stmt)

        message_list = []


        for item in res.all():
            
            from_user = await get_specific_user(user_id=item.from_id, session=session)
            to_user = await get_specific_user(user_id=item.to_id, session=session)

            from_username = from_user["data"][0]["username"]
            to_username = to_user["data"][0]["username"]

            if from_username == user.username:
                from_username = "you"
            else:
                to_username = "you"



            message_list.append({
                "from": from_username,
                "to": to_username,
                "message": item.message,
                "date": item.date
            })
        

        if not message_list:
            return {
                "status": 400,
                "data": None,
                "detail": "message not exist"
            }
        
        else:
            return {
                "status": 200,
                "data": message_list,
                "detail": None
            }


    except Exception as e:
        raise HTTPException(status_code=500, detail={
            "status": 500,
            "data": None,
            "detail": str(e)
        })


@router.get("/{to_id}")
async def get_specific_messages(
        to_id: int,
        session: AsyncSession=Depends(get_async_session),
        user=Depends(current_user)
):
    try:
        stmt = select(message).where(and_(message.c.from_id == user.id, message.c.to_id == to_id))
        result = await session.execute(stmt)

        message_list = []
        for item in result.all():
            message_list.append({
                "message": item[3],
                "date": item[4]
            })
        if not message_list:
            return {
                "status": 400,
                "data": None,
                "detail": "message not exist"
            }
        else:
            return {
                "status": 200,
                "data": message_list,
                "detail": None
            }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail={
            "status": 500,
            "data": None,
            "detail": str(e)
        })


@router.post("/send")
async def send_message(
        to_user: int,
        new_message: str,
        session: AsyncSession=Depends(get_async_session),
        user=Depends(current_user)
):
    try:
        stmt = insert(message).values(
            from_id=user.id,
            to_id=to_user,
            message=new_message
        )
        await session.execute(stmt)

        await session.commit()

        return {
            "status": 200,
            "data": None,
            "detail": "message send to user"
        }
        
        
    except Exception as e:
        raise HTTPException(status_code=500, detail={
            "status": 500,
            "data": None,
            "detail": str(e)
        })