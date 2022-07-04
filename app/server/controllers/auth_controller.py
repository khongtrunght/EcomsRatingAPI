from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from starlette import status

from server.auth.hashing import Hash
from server.auth.jwttoken import create_access_token, verify_token
from server.repositories import user_repo
from server.schemas.auth import SignupRequest


def ok(data=None):
    res = {'code': '1000', 'message': 'OK'}
    if data is not None:
        res['data'] = data
    return res


async def create_user(register_request: SignupRequest):
    user_doc = await user_repo.find_by_username(register_request.username)
    if user_doc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already exists")
    register_request.password = Hash.bcrypt(register_request.password)
    await user_repo.create(
        user=register_request.dict()
    )
    return ok()


async def login(login_request: OAuth2PasswordRequestForm = Depends()):
    user_doc = await user_repo.find_by_username(login_request.username)
    if not user_doc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    if not Hash.verify(user_doc['password'], login_request.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect password")
    access_token = create_access_token(data={"username": user_doc['username']})
    return {"access_token": access_token, "token_type": "bearer"}


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    return verify_token(token, credentials_exception)
