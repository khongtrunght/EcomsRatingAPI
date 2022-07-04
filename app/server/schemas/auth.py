from pydantic import BaseModel, Field


class SignupRequest(BaseModel):
    username: str = Field(..., regex="^\w{1,20}$")
    password: str


class LoginRequest(BaseModel):
    username: str = Field(..., regex="^\w{1,20}$")
    password: str
