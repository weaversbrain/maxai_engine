from fastapi import APIRouter, Depends
from app.core.database import Database
from typing import Union

router = APIRouter()

@router.post("/create")
async def createChat(userId: int = 0,userName: Union[str, None] = None,teacherName: Union[str, None] = None,teacherPersona: Union[str, None] = None):
  if userId: 
    db = Database('mysql')
    chatId = db.insertDB(table='Chat',colum='userId,userName,teacherName,teacherPersona',data="'"+str(userId)+"','"+userName+"','"+teacherName+"','"+teacherPersona+"'")
  return {"chatId":chatId}

@router.post("/module")
async def moduleStart():
  results = {"item": '1111111'}
  return results

@router.post("/addUserStatement")
async def addUserStatement():
  chatId = 1

  return chatId