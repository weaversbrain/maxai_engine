from core.database import Database
from model import ChatModel


def getChat(chatData: ChatModel):
    db = Database("mysql")
    sql = f"SELECT * from engine6.Chat WHERE id = {chatData['chatId']}"
    chatData = db.readDB(sql)
    print(chatData)
