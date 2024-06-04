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


def genChat(createChatData: CreateChatModel):
    db = Database("mysql")
    sql = f"""
        INSERT INTO chat 
        SET
            userId          = '{str(createChatData.userId)}',
            userName        = '{createChatData.userName}',
            teacherName     = '{createChatData.teacherName}',
            teacherPersona  = '{createChatData.teacherPersona.replace("'","\\'")}'
    """
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


def setChatStatement(
    chatId: int,
    messages: Union[str, None] = None,
    chatTurn: int = 0,
    currentModule: int = 0,
):
    db = Database("mysql")
    sql = (
        "UPDATE chat SET messages = '%s',chatTurn=%d,currentModule=%d  WHERE id = %d"
        % (json.dumps(messages).replace("'", "\\'"), chatTurn, currentModule, chatId)
    )
    chatId = db.updateDB(sql)
    return chatId


def getChat(chatId: int):
    db = Database("mysql")
    sql = f"SELECT * from engine6.chat WHERE id = {chatId}"
    chatData = db.readDB(sql)
    return chatData


def getListHistory(type: str, whereData: dict, pageData: Optional[dict] = None):
    whereSql = " WHERE 1=1"

    if whereData:
        if "chatId" in whereData:
            whereSql += f" AND A.chatId = '{whereData['chatId']}'"
        if "userId" in whereData:
            whereSql += f" AND A.userId = '{whereData['userId']}'"
        if "model" in whereData:
            whereSql += f" AND A.model = '{whereData['model']}'"

    db = Database("mysql")

    if type == "COUNT":
        sql = f"SELECT count(*) FROM engine6.chatHistory AS A {whereSql}"
        return db.readDB(sql)
    elif type == "LIST":
        sql = f"SELECT * from engine6.chatHistory AS A {whereSql} ORDER BY id DESC"
        return db.readDB(sql, "all")


def genHistory(createHistoryData: CreateHistoryModel):
    db = Database("mysql")
    sql = f"""
        INSERT INTO engine6.chatHistory 
        SET
            chatId           = '{createHistoryData['chatId']}',
            userId           = '{createHistoryData['userId']}',
            speaker          = '{createHistoryData['speaker']}',
            content          = '{createHistoryData['content'].replace("'","\\'")}',
            module           = '{createHistoryData['module']}'
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
