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
from prompt_base import reused_prompt, other_data
from openai import OpenAI
import datetime, os
from dotenv import load_dotenv
from model import *
from crud import *
from utility import *
from dotenv import dotenv_values
import os
import time
import sys

# 절대경로
abspath = os.path.dirname(os.path.abspath(__file__))
config = dotenv_values(abspath + "/.env")  # 환경변수 읽어오기


def runEngin6(moduleData: ModuleModel, type: str):
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
    if not chatInfo["chatTurn"]:
        chatTurn = 1
    else:
        chatTurn = chatInfo["chatTurn"] + 1

    ###########################
    # 2. initialize 작업
    ###########################
    renderedStr = renderTemplate("INITIAL", renderData)
    messageData = {"role": "system", "content": renderedStr}
    messages.append(messageData)

    renderData.update(reused_prompt)
    renderData.update(other_data)

    ###########################
    # 3. 현재 모듈의 히스토리 내역 삭제처리
    ###########################
    if type == "module":
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
        elif row["speaker"] == "SYSTEM":
            speaker = "system"

        messageData = {"role": speaker, "content": row["message"]}
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
    # 5. USER Answer 처리
    ###########################
    if type == "answer":
        messages.append({"role": "user", "content": moduleData.contents})
        createHistoryData = {
            "chatId": moduleData.chatId,
            "userId": moduleData.userId,
            "module": moduleData.module,
            "speaker": "USER",
            "content": moduleData.contents,
            "message": moduleData.contents,
        }
        genHistory(createHistoryData)

    ###########################
    # 6. LLM 처리
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

    gptMsgArr = []
    if response:
        print("-------------------------------")
        print(response.choices)
        print("-------------------------------")
        for choice in response.choices:  # 배열 형태로 문장이 여러개 줄 가능성 있음
            gptMsgArr.append(choice.message.content)  # 한문장 출력

    returnData = []
    for msg in gptMsgArr:
        print("-------------------------------")
        print(msg)
        print("-------------------------------")
        msg = msg.replace("\n\n", "\n")
        statementArr = msg.split("\n")

        for statement in statementArr:
            print(statement)
            splitData = splitTags(statement)
            returnData.append(splitData)

            if splitData["type"] == "user":
                speaker = "AI"
            elif splitData["type"] == "system":
                speaker = "SYSTEM"
            else:
                speaker = "AI"

            createHistoryData = {
                "chatId": moduleData.chatId,
                "userId": moduleData.userId,
                "module": moduleData.module,
                "speaker": speaker,
                "content": splitData["content"],
                "message": splitData["message"],
            }
            genHistory(createHistoryData)
        print("--------------------------------")

    ###########################
    # 7. 턴 업데이트
    ###########################
    updateData = {}
    updateData["chatTurn"] = chatTurn

    whereData = {}
    whereData["id"] = moduleData.chatId

    setChat(updateData, whereData)

    ###########################
    # 8. 반환
    ###########################
    return returnData
    # 데이터 가공 필요
