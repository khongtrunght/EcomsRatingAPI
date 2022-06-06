from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from server.routers import auth_router, rating_router, operation_router

app = FastAPI()

origins = ['https://localhost:8000']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

app.include_router(auth_router.router, prefix='/auth')
app.include_router(rating_router.router, prefix='/rating')
app.include_router(operation_router.router, prefix='/operation')
