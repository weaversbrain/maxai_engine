from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes.chat import chat

app = FastAPI()
app.include_router(chat)

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