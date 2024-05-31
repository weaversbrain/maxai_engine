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


def setChat(createChatData: CreateChatModel):
    db = Database("mysql")
    sql = f"""
        INSERT INTO Chat 
        SET
            userId          = '{str(createChatData.userId)}',
            userName        = '{createChatData.userName}',
            teacherName     = '{createChatData.teacherName}',
            teacherPersona  = '{createChatData.teacherPersona}'
    """
    chatId = db.insertDB(sql)
    return chatId


def updateChatStatement(
    chatId: int,
    messages: Union[str, None] = None,
    chatTurn: int = 0,
    currentModule: int = 0,
):
    db = Database("mysql")
    sql = (
        "UPDATE Chat SET messages = '%s',chatTurn=%d,currentModule=%d  WHERE id = %d"
        % (json.dumps(messages).replace("'", "\\'"), chatTurn, currentModule, chatId)
    )
    chatId = db.updateDB(sql)
    return chatId


def getChat(chatData: ChatModel):
    db = Database("mysql")
    sql = f"SELECT * from engine6.Chat WHERE id = {chatData['chatId']}"
    chatData = db.readDB(sql)
    return chatData


def getListHistory(type: str, whereData: dict, pageData: Optional[dict] = None):
    whereSql = " WHERE 1=1"

    if whereData:
        if "chatId" in whereData:
            whereSql += f" AND A.chatId = '{whereData['chatId']}'"
        if "model" in whereData:
            whereSql += f" AND A.model = '{whereData['model']}'"

    db = Database("mysql")

    if type == "COUNT":
        sql = f"SELECT count(*) FROM engine6.ChatHistory AS A {whereSql}"
        return db.readDB(sql)
    elif type == "LIST":
        sql = f"SELECT * from engine6.ChatHistory AS A {whereSql} ORDER BY id DESC"
        return db.readDB(sql, "all")
