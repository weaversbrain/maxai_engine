from fastapi import APIRouter, Depends
from app.core.database import Database
from typing import Union
import jinja2
import pandas as pd
import time
import numpy as np
import json
from prompt_base import other_data, reused_prompt, teacher_info, templates, user_info
from utils import process_tags, save_state, load_state, str2numtoken, token2cost
from openai import OpenAI
import os
from dotenv import load_dotenv

from app.process import userInfo

router = APIRouter()

@router.post("/create")
async def createChat(userId: int = 0,userName: Union[str, None] = None,teacherName: Union[str, None] = None,teacherPersona: Union[str, None] = None):


  if userId:
    db = Database('mysql')
    chatId = db.insertDB(table='Chat',colum='userId,userName,teacherName,teacherPersona',data="'"+str(userId)+"','"+userName+"','"+teacherName+"','"+teacherPersona+"'")


  return {"chatId":chatId}


@router.post("/module")
async def moduleStart(chatId: int = 0,module: Union[str, None] = None):

  if chatId == 0 or module == '':
      return {"result": False}




  return {"result": True}

@router.post("/addUserStatement")
async def addUserStatement():
  chatId = 1

  return chatId