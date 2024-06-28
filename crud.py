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

from database import Database
from model import *
from typing import Union
import json
from utility import *


def genChat(createChatData: CreateChatModel):
    db = Database("mysql")
    sql = """
        INSERT INTO chat 
        SET
            id              = %s,
            userId          = %s,
            lessonId        = %s,
            userName        = %s,
            teacherName     = %s,
            teacherPersona  = %s
    """

    params = (
        createChatData.chatId,
        str(createChatData.userId),
        str(createChatData.lessonId),
        createChatData.userName,
        createChatData.teacherName,
        escapeText(
            createChatData.teacherPersona.replace("\n", "").replace("\t", "")
        ),  # ' 문자 처리
    )

    chatId = db.insertDB(sql, params)
    return chatId


def setChat(updateData: dict, whereData: dict):
    updateSql = ""
    whereSql = " WHERE 1=1"
    updateParams = []
    whereParams = []

    if len(updateData) < 1 or len(whereData) < 1:
        return None

    # update 값 세팅
    for key, val in updateData.items():
        updateSql += f"{key} = %s, "
        updateParams.append(val)

    updateSql = updateSql[:-2]  # 마지막 ", " 제거

    # where 값 세팅
    for key, val in whereData.items():
        whereSql += f" AND {key} = %s"
        whereParams.append(val)

    db = Database("mysql")
    sql = f"""
            UPDATE
                engine6.chat    
            SET
                {updateSql}
            {whereSql}
    """
    # updateParams와 whereParams를 튜플로 변환
    params = tuple(updateParams + whereParams)

    db.updateDB(sql, params)


def setChatInfo(
    chatId: int,
    messages: Union[str, None] = None,
    pastConversation: Union[str, None] = None,
    chatTurn: int = 0,
    currentModule: int = 0,
):
    db = Database("mysql")
    sql = """
            UPDATE 
                chat 
            SET 
                messages = %s, 
                pastConversation=%s, 
                chatTurn=%s, 
                currentModule=%s,
                updatedAt = NOW()
            WHERE 
                id = %s
        """
    params = (
        json.dumps(messages, ensure_ascii=False),
        escapeText(pastConversation) if pastConversation else "",
        chatTurn,
        currentModule,
        chatId,
    )
    chatId = db.updateDB(sql, params)
    return chatId


def getChat(chatId: int):
    db = Database("mysql")
    sql = f"SELECT * from engine6.chat WHERE id = {chatId}"
    chatData = db.readDB(sql)
    return chatData


def getListHistory(whereData: dict):
    whereSql = " WHERE 1=1 AND del = 0"

    if whereData:
        if "chatId" in whereData:
            whereSql += f" AND A.chatId = '{whereData['chatId']}'"
        if "userId" in whereData:
            whereSql += f" AND A.userId = '{whereData['userId']}'"
        if "inModule" in whereData:
            if isinstance(whereData["inModule"], list):
                inModule = "','".join(whereData["inModule"])
                whereSql += f" AND A.module IN ('{inModule}')"
        if "module" in whereData:
            whereSql += f" AND A.module = '{whereData['module']}'"
        if "notModule" in whereData:
            whereSql += f" AND A.module != '{whereData['notModule']}'"

    db = Database("mysql")

    sql = f"SELECT * from engine6.chatHistory AS A {whereSql} ORDER BY id ASC"

    return db.readDB(sql, "all")


def genHistory(createHistoryData: CreateHistoryModel):
    db = Database("mysql")
    sql = """
        INSERT INTO engine6.chatHistory 
        SET
            chatId           = %s,
            userId           = %s,
            speaker          = %s,
            message          = %s,
            module           = %s,
            chatTurn         = %s
    """

    params = (
        createHistoryData["chatId"],
        createHistoryData["userId"],
        createHistoryData["speaker"],
        createHistoryData["message"],
        createHistoryData["module"],
        createHistoryData["chatTurn"],
    )

    insertId = db.insertDB(sql, params)
    return insertId


def setHistory(updateData: dict, whereData: dict) -> None:
    updateSql = ""
    whereSql = " WHERE 1=1"
    updateParams = []
    whereParams = []

    if len(updateData) < 1 or len(whereData) < 1:
        return None

    # update 값 세팅
    for key, val in updateData.items():
        updateSql += f"{key} = %s, "
        updateParams.append(val)

    updateSql = updateSql[:-2]  # 마지막 ", " 제거

    # where 값 세팅
    for key, val in whereData.items():
        whereSql += f" AND {key} = %s"
        whereParams.append(val)

    db = Database("mysql")
    sql = f"""
            UPDATE
                engine6.chatHistory    
            SET
                {updateSql}
            {whereSql}
    """

    # updateParams와 whereParams를 튜플로 변환
    params = tuple(updateParams + whereParams)

    db.updateDB(sql, params)


def getLessonInfo(lessonId: int):
    db = Database("mysql")

    sql = f"""
        SELECT 
            *
        FROM
            maxai_b2b_cms.maxai_lesson
        WHERE
            seq = '{lessonId}'
    """
    lessonInfo = db.readDB(sql)

    return lessonInfo


def getLessonExpression(lessonId: int):
    db = Database("mysql")

    sql = f"""
        SELECT 
            *
        FROM
            maxai_b2b_cms.maxai_lesson_etc
        WHERE
            gubun = 'expression'
            AND lSeq = '{lessonId}'
        LIMIT 1
    """
    expressionInfo = db.readDB(sql)

    return expressionInfo


def getListLessonModule(lessonId: int):
    db = Database("mysql")

    sql = f"""
        SELECT 
            A.*, B.code AS moduleName
        FROM
            maxai_b2b_cms.maxai_lesson_module AS A
            INNER JOIN maxai_b2b_cms.maxai_code AS B ON B.seq = A.cSeq
        WHERE
            A.lSeq = {lessonId}
            AND A.del = 0
    """
    moduleList = db.readDB(sql, "all")

    return moduleList


def getModule(moduleId: int):
    db = Database("mysql")

    sql = f"""
        SELECT 
            *
        FROM
            maxai_b2b_cms.maxai_module_part
        WHERE
            lmSeq = '{moduleId}'
    """
    lessonInfo = db.readDB(sql)

    return lessonInfo


def getLastChat(chatId: int, userId: int):
    db = Database("mysql")

    sql = f"""
        SELECT 
            *
        FROM
            engine6.chat
        WHERE
            userId = '{userId}'
            AND id < '{chatId}'
        ORDER BY
            id DESC
        LIMIT 1
    """
    lastChatInfo = db.readDB(sql)

    return lastChatInfo


def genChatCompletion(CreateChatCompletionModel):
    db = Database("mysql")
    sql = """
        INSERT INTO engine6.chatCompletionLog
        SET
            id                  = %s,
            chatId              = %s,
            request             = %s,
            response            = %s,
            returnData          = %s,
            model               = %s,
            created             = %s,
            completionTokens    = %s,
            promptTokens        = %s,
            totalRequestTokens  = %s,
            inputTokens         = %s,
            outputTokens        = %s,
            totalTokens         = %s,
            inputCost           = %s,
            outputCost          = %s,
            totalCost           = %s,
            llmTime             = %s,
            totalTime           = %s
    """

    params = (
        CreateChatCompletionModel["response"]["id"],
        CreateChatCompletionModel["chatId"],
        json.dumps(CreateChatCompletionModel["request"], ensure_ascii=False),
        json.dumps(CreateChatCompletionModel["response"], ensure_ascii=False),
        (
            json.dumps(CreateChatCompletionModel["returnData"], ensure_ascii=False)
            if "returnData" in CreateChatCompletionModel
            else ""
        ),
        CreateChatCompletionModel["response"]["model"],
        CreateChatCompletionModel["response"]["created"],
        CreateChatCompletionModel["response"]["usage"]["completion_tokens"],
        CreateChatCompletionModel["response"]["usage"]["prompt_tokens"],
        CreateChatCompletionModel["response"]["usage"]["total_tokens"],
        CreateChatCompletionModel["inputTokens"],
        CreateChatCompletionModel["outputTokens"],
        CreateChatCompletionModel["inputTokens"]
        + CreateChatCompletionModel["outputTokens"],
        "{:.4f}".format(CreateChatCompletionModel["inputCost"]),
        "{:.4f}".format(CreateChatCompletionModel["outputCost"]),
        "{:.4f}".format(
            CreateChatCompletionModel["inputCost"]
            + CreateChatCompletionModel["outputCost"]
        ),
        "{:.4f}".format(CreateChatCompletionModel["llmTime"]),
        "{:.4f}".format(CreateChatCompletionModel["totalTime"]),
    )

    insertId = db.insertDB(sql, params)
    return insertId


def setChatCompletion(updateData: dict, whereData: dict):
    updateSql = ""
    whereSql = " WHERE 1=1"
    updateParams = []
    whereParams = []

    if len(updateData) < 1 or len(whereData) < 1:
        return None

    # update 값 세팅
    for key, val in updateData.items():
        updateSql += f"{key} = %s, "
        updateParams.append(val)

    updateSql = updateSql[:-2]  # 마지막 ", " 제거

    # where 값 세팅
    for key, val in whereData.items():
        whereSql += f" AND {key} = %s"
        whereParams.append(val)

    db = Database("mysql")
    sql = f"""
            UPDATE
                engine6.chatCompletionLog    
            SET
                {updateSql}
            {whereSql}
    """
    # updateParams와 whereParams를 튜플로 변환
    params = tuple(updateParams + whereParams)

    db.updateDB(sql, params)


def getPromptList():
    db = Database("mysql")

    sql = f"""
        SELECT 
            a.*,
            (SELECT content FROM engine6.prompt b WHERE b.id = a.id) content 
        FROM 
            (
                SELECT 
                    name, 
                    MAX(VERSION) version, 
                    MAX(id) id, 
                    MAX(createdAt) createdAt 
                FROM 
                    engine6.prompt p 
                GROUP BY 
                    name
                ORDER BY 
                    LOWER(p.name) 
            ) a
    """
    promptList = db.readDB(sql, "all")

    return promptList
