from fastapi import Depends, HTTPException
from projects.models import project, ProjectCreate
from database import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from auth.base_config import current_user




async def create_project(
    name: str,
    description: str,
    needed_skills: str,
    session: AsyncSession = Depends(get_async_session),
):
    try:
        query = project.insert().values(name = name, description = description, needed_skills = needed_skills)
        result = await session.execute(query)
        return {
            "status": "success",
            "data": result.all,
            "detail": None
        }
    except:
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": None,
            "detail": None
        })