from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import delete, insert, select, update, func
from sqlalchemy.ext.asyncio import AsyncSession

from user.models import user
from friends.models import friend
from auth.base_config import current_user

from database import get_async_session
from user.router import get_specific_user


router = APIRouter(
    prefix="/friends",
    tags=["Friends"]
)


@router.delete("/delete")
async def delete_specific_friend(
    deleted_friend_id: int,
    user=Depends(current_user),
    session:AsyncSession=Depends(get_async_session)
):
    try:
        stmt = (
            update(friend).
            where(friend.c.user_id == user.id).
            values(list_of_friends=func.array_remove(friend.c.list_of_friends, deleted_friend_id))
        )
        await session.execute(stmt)
        await session.commit()
        return {
            "status": 200,
            "data": None,
            "detail": "friend has been removed from your list",
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail={
            "status": 200,
            "data": str(e),
            "detail": None
        })


@router.get("/")
async def get_list_of_friends(
    user=Depends(current_user),
    session:AsyncSession=Depends(get_async_session)
):
    try:
        stmt = select(friend).where(friend.c.user_id == user.id)
        result = await session.execute(stmt)
        friends_data = []
        for item in result.all():
            friends = item[2]
            
        for friend_id in friends:
            result = await get_specific_user(user_id=friend_id, session=session)
            friends_data.append(result["data"][0])


        return {
            "status": 200,
            "data": friends_data,
            "detail": None
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": None,
            "detail": str(e)
        })


@router.post("/add/{user_id}")
async def add_friend(
    new_friend_id: int,
    c_user=Depends(current_user),
    session: AsyncSession=Depends(get_async_session)
):
    try:
        ex = select(user).where(user.c.id == new_friend_id)
        res = await session.execute(ex)
        user_res = res.scalar_one_or_none()

        if user_res == None:
            return {
                "status": 400,
                "data": None,
                "detail": "user not exist"
            }

        else:

            stmt = update(friend).where(friend.c.user_id == c_user.id).values(
            list_of_friends=func.array_append(friend.c.list_of_friends, new_friend_id)
            )
            await session.execute(stmt)
            await session.commit()

            return {
                "status": 200,
                "data": None,
                "detail": "new friend add to your list"
            }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": None,
            "detail": str(e)
        })


@router.post("/update_friends_list")
async def update_friends_list(
    session: AsyncSession=Depends(get_async_session)
):
    try:
         # Получаем всех пользователей
        stmt_user = select(user)
        result_user = await session.execute(stmt_user)
        all_users = result_user.all()

        # Получаем существующие друзья для каждого пользователя и обновляем список друзей
        for u in all_users:
            user_id = u.id

            # Проверяем, есть ли уже запись о друзьях для данного пользователя
            stmt_existing_friends = select(friend).where(friend.c.user_id == user_id)
            result_existing_friends = await session.execute(stmt_existing_friends)
            existing_friends = result_existing_friends.scalar_one_or_none()

            if existing_friends is None:
                # Если записи о друзьях нет, создаем новую запись
                stmt_insert_friend = insert(friend).values(
                    user_id=user_id,
                    list_of_friends=[]
                )
                await session.execute(stmt_insert_friend)
            else:
                # Если запись о друзьях уже есть, пропускаем
                pass

        await session.commit()

        return {
            "status": 200,
            "data": None,
            "detail": "User's friends list update success"
        }
    
    
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": None,
            "detail": str(e)
        })