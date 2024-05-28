from database import Database
from model import ChatModel, CreateChatModel
from typing import Union

def setChat(createChatData: CreateChatModel):
    db = Database("mysql")
    qry = (
        "INSERT INTO Chat SET userId = '"
        + str(createChatData.userId)
        + "', userName = '"
        + createChatData.userName
        + "', teacherName = '"
        + createChatData.teacherName
        + "', teacherPersona = '"
        + createChatData.teacherPersona
        + "'"
    )
    chatId = db.insertDB(qry)
    return chatId


def getChat(chatData: ChatModel):
    db = Database("mysql")
    sql = f"SELECT * from engine6.Chat WHERE id = {chatData['chatId']}"
    chatData = db.readDB(sql)
    print(chatData)
