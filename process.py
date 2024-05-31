"""
+----------------------------------------------------------------------+
| Copyright (c) 2024 WeaversBrain. co. Ltd
+----------------------------------------------------------------------+
| 작업일 : 2024-05-23
| 파일설명 : 
+----------------------------------------------------------------------+
| 작업자 : 박범열
+----------------------------------------------------------------------+
| 수정이력
|
+----------------------------------------------------------------------+ 
"""

# from fastapi import FastAPI
# from prompt_base import *
from utility import renderTemplate
from openai import OpenAI
import datetime, os
from dotenv import load_dotenv
from model import CreateChatModel, ModuleModel
from crud import *
from utility import *
import sys
import time
import pytz
import jinja2
import json


def runEngin6(moduleData: ModuleModel):

    messages = []

    ###########################
    # initialize 작업
    ###########################

    ###########################
    # 히스토리 내역 가져옴
    ###########################
    historyData = {}
    historyData["chatId"] = moduleData.chatId
    historyData["userId"] = moduleData.userId

    historyList = getListHistory("LIST", historyData)  # 지금까지의 히스토리 내역

    ###########################
    # 현재 모듈 값 세팅
    ###########################

    renderedData = renderTemplate(moduleData.module, {})
    print(renderedData)

    ###########################
    # 반환
    ###########################
