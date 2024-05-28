from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# from fastapi.routing import APIRoute

from app.api.main import api_router

app = FastAPI()

origins = [
    "http://192.168.123.51",
    "http://192.168.123.51:8080",
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)