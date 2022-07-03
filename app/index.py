import requests
from fastapi import FastAPI
from fastapi.responses import HTMLResponse, RedirectResponse
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware import Middleware
from pydantic import BaseSettings
from server.routers import auth_router, rating_router, operation_router
from server.config.db import close_db


class Settings(BaseSettings):
	openapi_url: str = "/openapi.json"

test = requests.get("https://shopee.vn/api/v4/search/search_items?keyword=macbook%20pro&limit=2")
print(test.content)


settings = Settings()

middleware = [
	Middleware(CORSMiddleware, allow_origins=[''], allow_credentials=True, allow_methods=[''], allow_headers=['*'])]

app = FastAPI(middelware=middleware)


@app.get("/")
async def redirect_to_docs():
	return RedirectResponse("/docs")


app.include_router(auth_router.router, prefix='/auth')
app.include_router(rating_router.router, prefix='/rating')
app.include_router(operation_router.router, prefix='/operation')

app.add_event_handler("shutdown", close_db)
