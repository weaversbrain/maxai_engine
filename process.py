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
from dotenv import dotenv_values
import os
import time
import sys

# 절대경로
abspath = os.path.dirname(os.path.abspath(__file__))
config = dotenv_values(abspath + "/.env")  # 환경변수 읽어오기


def runEngin6(moduleData: ModuleModel):
    renderData = {}
    messages = []
    chatTurn = 0

    if config["MODEL_NAME"].startswith("gpt"):
        openai = OpenAI(
            api_key=config["API_KEY1"],
            # base_url="https://api.openai.com/v1",
        )
    else:
        openai = OpenAI(
            api_key=config["API_KEY2"],
            base_url="https://api.deepinfra.com/v1/openai",
        )

    ###########################
    # 1. chat Data 가져옴
    ###########################
    chatInfo = getChat(moduleData.chatId)

    if not chatInfo:
        return {"code": "E", "msg": "Chat정보가 없습니다."}

    renderData.update(chatInfo)
    chatTurn = chatInfo["chatTurn"]

    ###########################
    # 2. initialize 작업
    ###########################
    renderedStr = renderTemplate("INITIAL", renderData)
    messageData = {"role": "system", "content": renderedStr}
    messages.append(messageData)

    ###########################
    # 3. 현재 모듈의 히스토리 내역 삭제처리
    ###########################
    updateData = {}
    updateData["del"] = 1

    whereData = {}
    whereData["chatId"] = moduleData.chatId
    whereData["module"] = moduleData.module

    setHistory(updateData, whereData)

    ###########################
    # 4. 히스토리 내역 가져옴
    ###########################
    historyData = {}
    historyData["chatId"] = moduleData.chatId
    historyData["userId"] = moduleData.userId

    historyList = getListHistory("LIST", historyData)  # 지금까지의 히스토리 내역
    for row in historyList:
        speaker = "user"

        if row["speaker"] == "AI":
            speaker = "assistant"

        messageData = {"role": speaker, "content": row["content"]}
        messages.append(messageData)

    ###########################
    # 4. 현재 모듈 값 세팅
    ###########################
    renderData.update({"contents": moduleData.contents})
    renderedStr = renderTemplate(moduleData.module, renderData)

    messageData = {"role": "system", "content": renderedStr}
    messages.append(messageData)
    messageData = {"role": "system", "content": "(entered classroom)"}
    messages.append(messageData)

    ###########################
    # 5. LLM 처리
    ###########################
    messages.append({"role": "system", "content": f"ChatTurn: {chatTurn}"})
    start_time = time.time()

    response = openai.chat.completions.create(
        model=config["MODEL_NAME"],
        messages=messages,
        stream=False,
        max_tokens=200,
        temperature=0.5,
    )

    if response:
        for choice in response.choices:  # 배열 형태로 문장이 여러개 줄 가능성 있음
            print(choice.message.content)  # 한문장 출력

            # history insert 필요

    ###########################
    # 6. 반환
    ###########################

    # 데이터 가공 필요
