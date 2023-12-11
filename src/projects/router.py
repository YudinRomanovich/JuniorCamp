from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy import insert, select
from database import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from projects.models import project
from projects.schemas import ProjectCreate
from auth.base_config import current_user
from sqlalchemy.orm import Session


router = APIRouter(
    prefix="/project",
    tags=["Projects"]
)

@router.get("/get")
async def get_specific_progect(
    session: AsyncSession = Depends(get_async_session),
):
    try:
        result = await session.execute(select(project.c.id, project.c.name, project.c.description, project.c.author_id))
        dict_result = []
        for item in result.all():
            dict_result.append({
                "id": item[0],
                "name": item[1],
                "description": item[2],
                "author_id": item[3]
            })
         
        return dict_result
    except Exception:
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": None,
            "detail": None
        })


@router.post("/create")
async def add_specific_project(new_operation: ProjectCreate, session: AsyncSession = Depends(get_async_session)):
    stmt = insert(project).values(**new_operation.model_dump())
    await session.execute(stmt)
    await session.commit()
    return {"status": "success"}


# @router.get("/create_project")
# async def create_project(
#     name: str,
#     description: str,
#     needed_skills: str,
#     session: AsyncSession = Depends(get_async_session),
#     user = Depends(current_user)
# ):
#     try:
#         query = project.insert().values(name = name, description = description, needed_skills = needed_skills, )
#         result = await session.execute(query)
#         return {
#             "status": "success",
#             "data": result.all,
#             "detail": None
#         }
#     except:
#         raise HTTPException(status_code=500, detail={
#             "status": "error",
#             "data": None,
#             "detail": None
#         })