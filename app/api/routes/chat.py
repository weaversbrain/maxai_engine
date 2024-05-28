from fastapi import APIRouter
from app.core.database import Database
from typing import Union
from app.model import *
from app.crud import *

router = APIRouter()

@router.post("/createChat")
async def createChat(createChatData: CreateChatModel):
    if (
        createChatData["userId"]
        and createChatData["userName"]
        and createChatData["teacherName"]
        and createChatData["teacherPersona"]
    ):
        chatId = setChat(createChatData)
        return {"result": True, "chatId": chatId}
    else:
        return {"result": False}


@router.post("/module")
async def moduleStart(moduleData: ModuleModel):
    if moduleData["chatId"] == 0 or moduleData["module"] == "":
        return {"result": False}
    else:
        return {"result": True}


@router.post("/addUserStatement")
async def addUserStatement():
    chatId = 1
    return {"result": True}
