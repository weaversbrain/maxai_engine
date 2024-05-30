"""
+----------------------------------------------------------------------+
| Copyright (c) 2024 WeaversBrain. co. Ltd
+----------------------------------------------------------------------+
| 작업일 : 2024-05-23
| 파일설명 : 
+----------------------------------------------------------------------+
| 작업자 : 김용성, 박범열
+----------------------------------------------------------------------+
| 수정이력
|
+----------------------------------------------------------------------+ 
"""

from fastapi import APIRouter
#from database import Database
#from typing import Union
from model import CreateChatModel, ModuleModel
from crud import *
from process import *

chat = APIRouter(prefix='/chat', tags=['chat'])

@chat.post("/createChat")
#async def createChat(userId: int = 0,userName: Union[str, None] = None,teacherName: Union[str, None] = None,teacherPersona: Union[str, None] = None):
async def createChat(createChatData: CreateChatModel):
    if (
        createChatData.userId 
        and createChatData.userName
        and createChatData.teacherName
        and createChatData.teacherPersona
    ):
        # chat 생성
        chatId = setChat(createChatData)

        # 초기 AI prompt 가져오기
        # response = runEngin6({'userId':createChatData.userId,'chatId':chatId,'module':'initial','answer':''})

        return {"result": True, "chatId": chatId, "response": response}
    
    else:
        return {"result": False}

@chat.post("/startModule")
async def moduleStart(moduleData: ModuleModel):
    if moduleData.userId == 0 or moduleData.chatId == 0 or moduleData.module == "":
        return {"result": False}
    else:
        runEngin6(moduleData)
        return {"result": True}


@chat.post("/answerUser")
async def addUserStatement(moduleData: ModuleModel):
    if (
        moduleData.userId 
        and moduleData.chatId
        and moduleData.module
        and moduleData.userMessage
    ):
        response = runEngin6({'userId':moduleData.userId,'chatId':moduleData.chatId,'module':moduleData.module,'userMessage':moduleData.userMessage})

        return {"result": True, "chatId": moduleData.chatId, "response": response}
    
    else:
        return {"result": False}