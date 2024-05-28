from fastapi import APIRouter
#from app.core.database import Database
from typing import Union
from app.model import CreateChatModel, ModuleModel
from app.crud import *

router = APIRouter()

@router.post("/createChat")
async def createChat(userId: int = 0,userName: Union[str, None] = None,teacherName: Union[str, None] = None,teacherPersona: Union[str, None] = None):

    if (
        userId 
        and userName
        and teacherName
        and teacherPersona
    ):
        chatId = setChat(userId,userName,teacherName,teacherPersona)
        return {"result": True, "chatId": chatId}
    else:
        return {"result": False}

"""
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
async def createChat(userId: int = 0,userName: Union[str, None] = None,teacherName: Union[str, None] = None,teacherPersona: Union[str, None] = None):

    if (
        userId 
        and userName
        and teacherName
        and teacherPersona
    ):
"""

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
