from fastapi import APIRouter, Depends, HTTPException
from fastapi_cache.decorator import cache
from sqlalchemy import delete, insert, select, update
from database import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from projects.models import project
from projects.schemas import ProjectCreate
from auth.base_config import current_user


router = APIRouter(
    prefix="/projects",
    tags=["Projects"]
)


@router.delete("/delete")
async def delete_current_project(
    current_project_id: int,
    current_project_author_id: int, 
    user=Depends(current_user),
    session: AsyncSession = Depends(get_async_session)
):
    if current_project_author_id == user.id:
        try:
            stmt = (
                delete(project)
                .where(project.c.id == current_project_id)
            )

            await session.execute(stmt)
            await session.commit()
            return {
                "status": 200,
                "data": None,
                "detail": "project deleted"
            }

        except Exception:
            raise HTTPException(status_code=500, detail={
                "status": "error",
                "data": None,
                "detail": None
            })
    else:
        return {
            "status": "Access Denied",
            "data": None,
            "detail": "You are not author"
        }

    


@router.put("/edit")
async def edit_current_project(
    new_description: str,
    new_name: str,
    new_needed_skills: str,
    current_project_id: int,
    current_project_author_id: int, 
    user=Depends(current_user),
    session: AsyncSession=Depends(get_async_session),
):
    if current_project_author_id == user.id:
        try:
            stmt = (
                update(project)
                .where(project.c.id == current_project_id)
                .values(
                    name=new_name,
                    description=new_description,
                    needed_skills=new_needed_skills
                )
            )
            await session.execute(stmt)
            await session.commit()
            return {
                "status": 200,
                "data": None,
                "detail": "project updated"
            }

        except Exception:
            raise HTTPException(status_code=500, detail={
                "status": "error",
                "data": None,
                "detail": None
            })
    else:
        return {
            "status": "Access Denied",
            "data": None,
            "detail": "You are not author"
        }


@router.get("/get")
@cache(expire=60)
async def get_all_projects(
    session: AsyncSession = Depends(get_async_session),
):
    try:
        result = await session.execute(select(project.c.id, project.c.name, project.c.description, project.c.author_id, project.c.needed_skills))
        dict_result = []
        for item in result.all():
            dict_result.append({
                "id": item[0],
                "name": item[1],
                "description": item[2],
                "author_id": item[3],
                "needed_skills": item[4],
            })
         
        return {
            "status": "200",
            "data": dict_result,
            "detail": None
        }
    except Exception:
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": None,
            "detail": None
        })


@router.get("/{project_id}")
async def get_specific_project(project_id: int, session: AsyncSession = Depends(get_async_session)):
    try:
        result = await session.execute(select(project).where(project.c.id == project_id))
        dict_result = []
        for item in result.all():
            dict_result.append({
                "id": item[0],
                "name": item[1],
                "description": item[2],
                "author_id": item[3]
            })
        return {
            "status": "200",
            "data": dict_result[0],
            "detail": None
        }
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
    return {
        "status": "success",
        "data": "Project has been created",
        "detail": None
    }