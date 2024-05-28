from database import Database
from model import ChatModel, CreateChatModel
from typing import Union

def setChat(userId: int = 0,userName: Union[str, None] = None,teacherName: Union[str, None] = None,teacherPersona: Union[str, None] = None):
    db = Database("mysql")
    qry = (
        "INSERT INTO Chat SET userId = '"
        + str(userId)
        + "', userName = '"
        + userName
        + "', teacherName = '"
        + teacherName
        + "', teacherPersona = '"
        + teacherPersona
        + "'"
    )
    chatId = db.insertDB(qry)
    return chatId


def getChat(chatData: ChatModel):
    db = Database("mysql")
    sql = f"SELECT * from engine6.Chat WHERE id = {chatData['chatId']}"
    chatData = db.readDB(sql)
    print(chatData)
