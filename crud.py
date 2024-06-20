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
            id              = '{}',
            userId          = '{}',
            lessonId        = '{}',
            userName        = '{}',
            teacherName     = '{}',
            teacherPersona  = '{}'
    """.format(
        createChatData.chatId,
        str(createChatData.userId),
        str(createChatData.lessonId),
        createChatData.userName,
        createChatData.teacherName,
        escapeText(createChatData.teacherPersona),  # ' 문자 처리
    )

    chatId = db.insertDB(sql)
    return chatId


def setChat(updateData: dict, whereData: dict):
    updateSql = ""
    whereSql = " WHERE 1=1"

    if len(updateData) < 1 or len(whereData) < 1:
        return None

    # update 값 세팅
    for key, val in updateData.items():
        updateSql += f"{key} = '{val}',"

    updateSql = updateSql[:-1]  # 마지막 , 제거

    # where 값 세팅
    for key, val in whereData.items():
        whereSql += f" AND {key} = '{val}'"

    db = Database("mysql")
    sql = f"""
            UPDATE
                engine6.chat    
            SET
                {updateSql}
            {whereSql}
    """
    db.updateDB(sql)


def setChatInfo(
    chatId: int,
    messages: Union[str, None] = None,
    createdGreetings: Union[str, None] = None,
    chatTurn: int = 0,
    currentModule: int = 0,
):
    db = Database("mysql")
    sql = (
        """UPDATE chat SET messages = '%s',createdGreetings='%s', chatTurn=%d,currentModule='%s'  WHERE id = %d"""
        % (
            escapeText(json.dumps(messages, ensure_ascii=False)),
            escapeText(createdGreetings) if createdGreetings else "",
            chatTurn,
            currentModule,
            chatId,
        )
    )
    chatId = db.updateDB(sql)
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
    sql = f"""
        INSERT INTO engine6.chatHistory 
        SET
            chatId           = '{createHistoryData['chatId']}',
            userId           = '{createHistoryData['userId']}',
            speaker          = '{createHistoryData['speaker']}',
            message          = '{createHistoryData['message']}',
            module           = '{createHistoryData['module']}',
            chatTurn         = '{createHistoryData['chatTurn']}'
    """
    insertId = db.insertDB(sql)
    return insertId


def setHistory(updateData: dict, whereData: dict):
    updateSql = ""
    whereSql = " WHERE 1=1"

    if len(updateData) < 1 or len(whereData) < 1:
        return None

    # update 값 세팅
    for key, val in updateData.items():
        updateSql += f"{key} = '{val}',"

    updateSql = updateSql[:-1]  # 마지막 , 제거

    # where 값 세팅
    for key, val in whereData.items():
        whereSql += f" AND {key} = '{val}'"

    db = Database("mysql")
    sql = f"""
            UPDATE
                engine6.chatHistory    
            SET
                {updateSql}
            {whereSql}
    """
    db.updateDB(sql)


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
            AND seq = '{lessonId}'
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


def genChatCompletion(chatId, request, response):
    db = Database("mysql")
    sql = """
        INSERT INTO engine6.chatCompletionLog 
        SET
            id                  = '{}',
            chatId              = '{}',
            request             = '{}',
            response            = '{}',
            model               = '{}',
            created             = '{}',
            completion_tokens   = '{}',
            prompt_tokens       = '{}',
            total_tokens        = '{}'
    """.format(
        response["id"],
        chatId,
        escapeText(json.dumps(request, ensure_ascii=False)),
        escapeText(json.dumps(response, ensure_ascii=False)),
        response["model"],
        response["created"],
        response["usage"]["completion_tokens"],
        response["usage"]["prompt_tokens"],
        response["usage"]["total_tokens"],
    )
    insertId = db.insertDB(sql)
    return insertId
