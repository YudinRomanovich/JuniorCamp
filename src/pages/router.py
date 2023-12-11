import bcrypt
from fastapi import APIRouter, Depends, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from auth.base_config import current_user
from projects.router import get_specific_progect

router = APIRouter(
    prefix="",
    tags=["Pages"]
)

templates = Jinja2Templates(directory="templates")

@router.get("/projects")
async def get_project_page(request: Request, projects=Depends(get_specific_progect)):
    print(projects)
    return templates.TemplateResponse("projects.html", {"request": request, "projects": projects})

@router.get("/feed")
async def get_base_page(request: Request):
    return templates.TemplateResponse("feed.html", {"request": request})

@router.get("/register")
def get_register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@router.get("/login")
def get_login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@router.get("/validation")
async def get_validation(request: Request, email: str, password: str, user=Depends(current_user)):
    # Валидация данных email и password
    if email == user.email and bcrypt.checkpw(password.encode(), user.hashed_password.encode()):
        return RedirectResponse(url=f"/{user.username}")
    else: 
        {
            "status": "400",
            "detail": "email or password dont valid",
            "data": None
        }

@router.get("/{username}")
async def get_account(request: Request, user=Depends(current_user)):
    return templates.TemplateResponse("account.html", {"request": request, "user": user})

