from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes.chat import chat

app = FastAPI()
SWAGGER_HEADERS = {
    "title": "MaxAI Engine6",
    "description": "## SWAGGER - MaxAI Engine6.",
}

app = FastAPI(
    swagger_ui_parameters={
        "deepLinking": True,
        "displayRequestDuration": True,
        "docExpansion": "none",
        "operationsSorter": "method",
        "filter": False,
        "tagsSorter": "alpha",
        "syntaxHighlight.theme": "tomorrow-night",
    },
    **SWAGGER_HEADERS
)

app.include_router(chat)

# Set all CORS enabled origins
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
