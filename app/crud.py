from core.database import Database
from model import ChatModel, createChatModel


def setChat(createChatData: createChatModel):
    db = Database('mysql')
    qry = "INSERT INTO Chat SET userId = '"+ createChatData['userId'] +"', userName = '"+ createChatData['userName'] +"', teacherName = '"+ createChatData['teacherName'] +"', createChatData['teacherPersona'] = '"+ teacherPersona +"'"
    chatId = db.insertDB(qry)
    return chatId

def getChat(chatData: ChatModel):
    db = Database("mysql")
    sql = f"SELECT * from engine6.Chat WHERE id = {chatData['chatId']}"
    chatData = db.readDB(sql)
    print(chatData)
