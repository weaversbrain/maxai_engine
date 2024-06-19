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

# from database import Database
# from typing import Union
from model import CreateChatModel, ModuleModel, CreateFeedbackModel
from crud import *
from process import *

chat = APIRouter(prefix="/chat", tags=["chat"])


@chat.post("/createChat")
# async def createChat(userId: int = 0,userName: Union[str, None] = None,teacherName: Union[str, None] = None,teacherPersona: Union[str, None] = None):
async def createChat(createChatData: CreateChatModel):

    if (
        not createChatData.lessonId
        or not createChatData.userId
        or not createChatData.userName
        or not createChatData.teacherName
        or not createChatData.teacherPersona
    ):
        returnData = {"code": "E", "msg": "필수값 누락"}
        return returnData

    # 초기 AI prompt 가져오기
    # response = runEngin6({'userId':createChatData.userId,'chatId':chatId,'module':'initial','answer':''})

    chatId = genChat(createChatData)  # chat 생성
    returnData = {"code": "E", "msg": "채팅 생성 실패", "chatId": None}
    if chatId:
        returnData = {"code": "Y", "msg": "성공", "chatId": chatId}

    return returnData


@chat.post("/startModule")
async def moduleStart(moduleData: ModuleModel):
    if not moduleData.moduleId or not moduleData.chatId:
        return {"result": False}
    else:
        returnData = runEngin6(moduleData, "module")
        return {"result": True, "data": returnData}


@chat.post("/answerUser")
async def addUserStatement(moduleData: ModuleModel):
    if not moduleData.moduleId or not moduleData.chatId:
        return {"result": False}
    else:

        if not moduleData.userAnswer or moduleData.userAnswer == "":
            moduleData.userAnswer = (
                "(said nothing - maybe due to bad internet connection)"
            )

        returnData = runEngin6(moduleData, "answer")
        return {"result": True, "data": returnData}


@chat.post("/moduleList")
async def moduleList(moduleListData: ModuleListData):
    return getListLessonModule(moduleListData.lessonId)


@chat.post("/createFeedback")
async def createFeedback(createFeedbackModel: CreateFeedbackModel):
    if not createFeedbackModel.userId or not createFeedbackModel.chatId:
        return {"code": "E", "msg": "필수값 누락"}

    return createFeedback(createFeedbackModel)
