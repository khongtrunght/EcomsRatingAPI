from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer

from server.controllers.auth_controller import get_current_user
from server.controllers import auth_controller
from server.schemas.auth import SignupRequest

router = APIRouter(tags = ["Auth"])  # , dependencies=[Depends(get_current_user)])


@router.post("/create-user", dependencies=[Depends(get_current_user)])
async def signup(request: SignupRequest):
    return await auth_controller.create_user(request)


@router.post("/login", include_in_schema = False)
async def login(request: OAuth2PasswordRequestForm = Depends()):
    return await auth_controller.login(request)
