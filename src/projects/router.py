from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import insert, select
from database import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from projects.models import project
from projects.schemas import ProjectCreate


router = APIRouter(
    prefix="/projects",
    tags=["Projects"]
)


@router.get("/get")
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