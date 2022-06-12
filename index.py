from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware import Middleware
from pydantic import BaseSettings
from server.routers import auth_router, rating_router, operation_router

class Settings(BaseSettings):
    openapi_url: str = "/openapi.json"

settings = Settings()

middleware = [ Middleware(CORSMiddleware, allow_origins=[''], allow_credentials=True, allow_methods=[''], allow_headers=['*'])]

app = FastAPI(middelware = middleware, openapi_url = settings.openapi_url)

app.include_router(auth_router.router, prefix='/auth')
app.include_router(rating_router.router, prefix='/rating')
app.include_router(operation_router.router, prefix='/operation')
