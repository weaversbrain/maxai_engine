from app.database import Database
from app.model import ChatModel, CreateChatModel


def setChat(createChatData):
    db = Database("mysql")
    qry = (
        "INSERT INTO Chat SET userId = "
        + str(createChatData.userId)
        + ", userName = '"
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
