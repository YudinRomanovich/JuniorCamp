import os
from fastapi import FastAPI
from fastapi.responses import RedirectResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi_users import FastAPIUsers
from auth.manager import get_user_manager
from user.schemas import UserCreate, UserRead
from auth.base_config import auth_backend
from pages.router import router as router_base
from projects.router import router as router_proj
from user.router import router as router_user
from friends.router import router as router_friends
from message.router import router as router_message

app = FastAPI()

static_dir = os.path.join(os.path.dirname(__file__), 'static')
app.mount("/static", StaticFiles(directory=static_dir), name="static")

favicon_path = 'static/favicon.ico'

app.include_router(router_user)
app.include_router(router_base)
app.include_router(router_proj)
app.include_router(router_friends)
app.include_router(router_message)


fastapi_users = FastAPIUsers(
    get_user_manager,
    [auth_backend],
)


@app.get('/favicon.ico', include_in_schema=False)
async def favicon():
    return FileResponse(favicon_path)


@app.get("/")
async def get_redirect():
    return RedirectResponse(url="/login")


app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)


app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)