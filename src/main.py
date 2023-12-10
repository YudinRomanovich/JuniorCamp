from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from fastapi_users import FastAPIUsers
from auth.manager import get_user_manager
from auth.schemas import UserCreate, UserRead
from auth.base_config import auth_backend

from pages.router import router as router_base

app = FastAPI()

app.include_router(router_base)

fastapi_users = FastAPIUsers(
    get_user_manager,
    [auth_backend],
)

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
