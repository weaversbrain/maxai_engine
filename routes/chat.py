from fastapi import APIRouter
#from database import Database
from typing import Union
from model import CreateChatModel, ModuleModel
from crud import *

chat = APIRouter(prefix='/chat', tags=['chat'])

@chat.post("/create")
#async def createChat(userId: int = 0,userName: Union[str, None] = None,teacherName: Union[str, None] = None,teacherPersona: Union[str, None] = None):
async def createChat(createChatData: CreateChatModel):
    if (
        createChatData.userId 
        and createChatData.userName
        and createChatData.teacherName
        and createChatData.teacherPersona
    ):
        chatId = setChat(createChatData)
        return {"result": True, "chatId": chatId}
    else:
        return {"result": False}

@chat.post("/module")
async def moduleStart(moduleData: ModuleModel):
    if moduleData["chatId"] == 0 or moduleData["module"] == "":
        return {"result": False}
    else:
        return {"result": True}


@chat.post("/addUserStatement")
async def addUserStatement():
    chatId = 1
    return {"result": True}
