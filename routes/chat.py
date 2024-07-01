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

from model import CreateChatModel, ModuleModel, CreateFeedbackModel
from crud import *
from process import *
from feedback import createFeedback

chat = APIRouter(prefix="/chat", tags=["chat"])


@chat.post("/createChat")
async def createChat(createChatData: CreateChatModel):

    if (
        not createChatData.chatId
        or not createChatData.lessonId
        or not createChatData.userId
        or not createChatData.userName
        or not createChatData.teacherName
        or not createChatData.teacherPersona
    ):
        returnData = {"code": "E", "msg": "필수값 누락"}
        return returnData

    # 채팅 중복 채크
    chatInfo = getChat(createChatData.chatId)
    if chatInfo:
        return {"code": "E", "msg": "ChatId 중복", "chatId": None}

    # chat 생성
    genChat(createChatData)

    # 채팅 생성 되었는지 확인
    chatInfo = getChat(createChatData.chatId)
    if not chatInfo:
        return {"code": "E", "msg": "채팅 생성 실패", "chatId": None}

    return {"code": "Y", "msg": "성공", "chatId": createChatData.chatId}


@chat.post("/startModule")
async def moduleStart(moduleData: ModuleModel):
    if not moduleData.moduleId or not moduleData.chatId:
        return {"code": "E", "msg": "필수값 누락"}
    else:
        returnData = runEngin6(moduleData, "module")

        if not returnData:
            return {"code": "E01", "msg": "response값이 없습니다."}

        if not "responseData" in returnData:
            return {"code": "E02", "msg": "response값이 없습니다."}

        return {"result": True, "data": returnData["responseData"]}


@chat.post("/answerUser")
async def addUserStatement(moduleData: ModuleModel):
    if not moduleData.moduleId or not moduleData.chatId:
        return {"result": False}
    else:

        if not moduleData.userAnswer or moduleData.userAnswer == "":
            moduleData.userAnswer = (
                "(said nothing - maybe due to bad internet connection)"
            )

        result = runEngin6(moduleData, "answer")

        if not result:
            return {"code": "E01", "msg": "response값이 없습니다."}

        if not "responseData" in result:
            return {"code": "E02", "msg": "response값이 없습니다."}

        returnData = {"result": True, "data": result["responseData"]}

        if "userChatStatementId" in result:
            returnData.update({"userChatStatementId": result["userChatStatementId"]})

        return returnData


@chat.post("/moduleList")
async def moduleList(moduleListData: ModuleListData):
    return getListLessonModule(moduleListData.lessonId)


@chat.post("/createFeedback")
async def feedbackCreate(createFeedbackModel: CreateFeedbackModel):
    if not createFeedbackModel.userId or not createFeedbackModel.chatId:
        return {"code": "E", "msg": "필수값 누락"}

    returnData = createFeedback(createFeedbackModel)

    if not returnData:
        return {"code": "E", "msg": "feedback데이터가 없습니다."}

    return returnData
