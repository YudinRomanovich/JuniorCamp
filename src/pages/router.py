import bcrypt
from fastapi import APIRouter, Depends, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from auth.base_config import current_user
from projects.router import get_all_projects, get_specific_project
from user.router import get_specific_user
from friends.router import get_list_of_friends
from message.router import get_messages, get_specific_messages


router = APIRouter(
    prefix="",
    tags=["Pages"]
)


def get_user_username(user=Depends(current_user)) -> str:
    username = user.username
    return username


templates = Jinja2Templates(directory="templates")


@router.get("/messages/{user_id}")
async def get_dialogue_page(request: Request, user=Depends(current_user), c_messages=Depends(get_specific_messages)):
    
    return templates.TemplateResponse("dialogue.html", {"request": request, "messages": c_messages, "user": user})


@router.get("/messages")
async def get_messages_page(request: Request, messages=Depends(get_messages), user=Depends(current_user)):
    
    return templates.TemplateResponse("messages.html", {"request": request, "messages": messages, "user": user})


@router.get("/friends")
async def get_friends_page(request: Request, c_user=Depends(get_list_of_friends), user=Depends(current_user)):

    return templates.TemplateResponse("friends.html", {"request": request, "c_user": c_user["data"], "user": user})


@router.get("/edit")
async def get_edit_page(request: Request, user=Depends(current_user)):

    return templates.TemplateResponse("edit_profile.html", {"request": request, "user": user})


@router.get("/projects")
async def get_project_page(request: Request, projects=Depends(get_all_projects), user=Depends(current_user)):

    return templates.TemplateResponse("projects.html", {"request": request, "projects": projects["data"], "user": user})


@router.get("/projects/view/{project_id}")
async def get_view_project_page(request: Request, project=Depends(get_specific_project), user=Depends(current_user)):

    return templates.TemplateResponse("project_view.html", {"request": request, "project": project["data"], "user": user})


@router.get("/projects/new")
async def get_create_project_page(request: Request, user=Depends(current_user)):

    return templates.TemplateResponse("project_create.html", {"request": request, "user": user})


@router.get("/feed")
async def get_base_page(request: Request, user=Depends(current_user)):

    return templates.TemplateResponse("feed.html", {"request": request, "user": user})


@router.get("/register")
def get_register_page(request: Request):

    return templates.TemplateResponse("register.html", {"request": request})


@router.get("/login")
def get_login_page(request: Request):

    return templates.TemplateResponse("login.html", {"request": request})


@router.get("/validation")
async def get_validation(email: str, password: str, user=Depends(current_user)):
    # Валидация данных email и password
    if email == user.email and bcrypt.checkpw(password.encode(), user.hashed_password.encode()):
        return RedirectResponse(url=f"/{user.username}")
    else: 
        {
            "status": "400",
            "detail": "email or password dont valid",
            "data": None
        }


@router.get("/{username}/edit")
async def get_edit_account(request: Request, user=Depends(current_user)):
    
    return templates.TemplateResponse("edit_profile.html", {"request": request, "user": user})
    

@router.get("/{username}")
async def get_account(request: Request, username: str, user=Depends(current_user), another_user=Depends(get_specific_user)):
    try:
        if another_user["data"] is []:
            return templates.TemplateResponse("account.html", {"request": request, "user": user})
        elif another_user["data"][0]["username"] == user.username:
            return templates.TemplateResponse("account.html", {"request": request, "user": user})
        else:
            return templates.TemplateResponse("another_user_account.html", {"request": request, "another_user": another_user["data"][0], "user": user})
        
    except:
        return {
            "status": "Error",
            "data": None,
            "detail": None
        }