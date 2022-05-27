from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from server.controllers import auth_controller
from server.schemas.auth import SignupRequest

router = APIRouter(tags=["auth"])


@router.post("/login")
async def login(request: OAuth2PasswordRequestForm = Depends()):
    return await auth_controller.login(request)


@router.post("/signup")
async def signup(signup_info: SignupRequest):
    return await auth_controller.create_user(signup_info)