from fastapi import FastAPI

import models
from database import engine
models.Base.metadata.create_all(bind=engine)

from board import board_router

#app = FastAPI()
SWAGGER_HEADERS = {
    "title": "MaxAI Engine6",
    #"version": "100.100.100",
    "description": "## SWAGGER 문서 변경 \n - 이영찬 테스트 입니다.",
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

app.include_router(board_router.app, tags=["board"])

@app.get("/")
def read_root():
    return {"Hello": "World"}