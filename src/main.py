from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi_users import FastAPIUsers
from auth.manager import get_user_manager
from auth.schemas import UserCreate, UserRead
from auth.base_config import auth_backend

from pages.router import router as router_base
from projects.router import router as router_proj


app = FastAPI()

app.include_router(router_base)
app.include_router(router_proj)


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
