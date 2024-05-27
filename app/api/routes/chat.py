from fastapi import APIRouter
from app.core.database import Database
from typing import Union
from model import createChatModel
from crud import *

router = APIRouter()


@router.post("/createChat")
async def createChat(createChatData: createChatModel):
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
async def moduleStart(chatId: int = 0, module: Union[str, None] = None):
    if chatId == 0 or module == "":
        return {"result": False}
    else:
        return {"result": True}


@router.post("/addUserStatement")
async def addUserStatement():
    chatId = 1
    return {"result": True}
