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
    sql = f'''
        INSERT INTO chat 
        SET
            lessonId        = '{str(createChatData.lessonId)}',
            userId          = '{str(createChatData.userId)}',
            userName        = '{createChatData.userName}',
            teacherName     = '{createChatData.teacherName}',
            teacherPersona  = '{createChatData.teacherPersona.replace("'","\\'")}'
    '''
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
    chatTurn: int = 0,
    currentModule: int = 0,
):
    db = Database("mysql")
    sql = (
        """UPDATE chat SET messages = '%s',chatTurn=%d,currentModule='%s'  WHERE id = %d"""
        % (
            escapeText(json.dumps(messages, ensure_ascii=False)),
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


def getListHistory(type: str, whereData: dict, pageData: Optional[dict] = None):
    whereSql = " WHERE 1=1 AND del = 0"

    if whereData:
        if "chatId" in whereData:
            whereSql += f" AND A.chatId = '{whereData['chatId']}'"
        if "userId" in whereData:
            whereSql += f" AND A.userId = '{whereData['userId']}'"
        if "module" in whereData:
            whereSql += f" AND A.module = '{whereData['module']}'"
        if "notModule" in whereData:
            whereSql += f" AND A.module != '{whereData['notModule']}'"

    db = Database("mysql")

    if type == "COUNT":
        sql = f"SELECT count(*) FROM engine6.chatHistory AS A {whereSql}"
        return db.readDB(sql)
    elif type == "LIST":
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


def getLessonModuleList(lessonId: int):
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


def getModuleInfo(moduleId: int):
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
