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
from utility import *
from prompt_base import reused_prompt, other_data
from openai import OpenAI
import datetime, os
from dotenv import load_dotenv
from model import *
from crud import *
from dotenv import dotenv_values
import os
import time
import sys
from workReturnData import *

# 절대경로
abspath = os.path.dirname(os.path.abspath(__file__))
config = dotenv_values(abspath + "/.env")  # 환경변수 읽어오기


def runEngin6(moduleData: ModuleModel, type: str):

    ###########################
    # 초기 세팅
    ###########################
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

    renderData = {}
    messages = []
    totalChatTurn = 0
    pastConversation = ""

    saveFile = f"log/chat_{moduleData.chatId}.json"  # 로그 파일

    renderData.update(reused_prompt)
    renderData.update(other_data)

    chatInfo = getChat(moduleData.chatId)  # chat Info
    moduleInfo = getModule(moduleData.moduleId)  # module Info
    lessonInfo = getLessonInfo(chatInfo["lessonId"])  # lesson Info
    expression = getLessonExpression(chatInfo["lessonId"])  # lesson expression

    todayExpression = expression["property"] if expression else ""

    if not todayExpression:
        return {"code": "E", "msg": "오늘의 표현 정보가 없습니다."}

    renderData.update({"todayExpression": todayExpression})

    ###########################
    # pastConversation 추출
    ###########################
    if moduleInfo["module"] == "E6_SMALL_TALK":
        lastChat = getLastChat(chatInfo["id"], chatInfo["userId"])
        if lastChat and lastChat["pastConversation"]:
            renderData.update({"pastConversation": lastChat["pastConversation"]})

    ###########################
    # 1. chat Data 가져옴
    ###########################

    if not chatInfo:
        return {"code": "E", "msg": "Chat정보가 없습니다."}

    renderData.update(chatInfo)
    if not chatInfo["chatTurn"]:
        totalChatTurn = 0
    else:
        totalChatTurn = chatInfo["chatTurn"]

    if chatInfo["pastConversation"]:
        pastConversation = chatInfo["pastConversation"]

    ###########################
    # 2. initialize 작업
    ###########################
    renderedStr = renderTemplate("INITIAL", renderData)
    messageData = {
        "role": "system",
        "content": renderedStr,
    }
    messages.append(messageData)

    ###########################
    # 3. 현재 모듈의 히스토리 내역 삭제처리
    ###########################
    if type == "module":
        updateData = {}
        updateData["del"] = 1

        whereData = {}
        whereData["chatId"] = moduleData.chatId
        whereData["module"] = moduleInfo["module"]

        setHistory(updateData, whereData)

    ###########################
    # 과거 히스토리 내역 가져옴
    ###########################
    historyData = {}
    historyData["chatId"] = moduleData.chatId
    historyData["userId"] = chatInfo["userId"]
    historyData["notModule"] = moduleInfo["module"]

    historyList = getListHistory(historyData)  # 지금까지의 히스토리 내역
    for row in historyList:
        speaker = "user"

        if row["speaker"] == "AI" or row["speaker"] == "SYSTEM":
            speaker = "assistant"

        messageData = {
            "role": speaker,
            "content": row["message"],
        }
        messages.append(messageData)

    ###########################
    # 현재 모듈 값 세팅
    ###########################
    moduleInfo = getModule(moduleData.moduleId)
    renderData.update({"contents": moduleInfo["content"]})
    renderedStr = renderTemplate(moduleInfo["module"], renderData)

    messageData = {
        "role": "system",
        "content": renderedStr,
    }
    messages.append(messageData)

    if totalChatTurn == 0:
        # messageData = {"role": "user", "content": "(entered classroom)"}
        # messages.append(messageData)

        createHistoryData = {
            "chatId": moduleData.chatId,
            "userId": chatInfo["userId"],
            "module": moduleInfo["module"],
            "speaker": "USER",
            "content": "(entered classroom)",
            "message": "(entered classroom)",
            "chatTurn": 0,
        }
        genHistory(createHistoryData)

    ###########################
    # 히스토리 내역 가져옴
    ###########################
    historyData = {}
    historyData["chatId"] = moduleData.chatId
    historyData["userId"] = chatInfo["userId"]
    historyData["module"] = moduleInfo["module"]

    historyList = getListHistory(historyData)  # 지금까지의 히스토리 내역
    curChatTurn = 0
    for row in historyList:
        speaker = "user"

        if row["speaker"] == "AI" or row["speaker"] == "SYSTEM":
            speaker = "assistant"

        messageData = {
            "role": speaker,
            "content": row["message"],
        }
        messages.append(messageData)

        if row["chatTurn"]:
            curChatTurn = row["chatTurn"]

    ###########################
    # 5. USER Answer 처리
    ###########################
    if type == "answer":
        totalChatTurn = totalChatTurn + 1
        curChatTurn = curChatTurn + 1
        messages.append({"role": "user", "content": moduleData.userAnswer})
        createHistoryData = {
            "chatId": moduleData.chatId,
            "userId": chatInfo["userId"],
            "module": moduleInfo["module"],
            "speaker": "USER",
            "message": escapeText(moduleData.userAnswer),
            "chatTurn": curChatTurn,
        }
        genHistory(createHistoryData)

    ###########################
    # 6. LLM 처리
    ###########################
    messages.append({"role": "system", "content": f"ChatTurn: {curChatTurn}"})
    start_time = time.time()

    response = openai.chat.completions.create(
        model=config["MODEL_NAME"],
        messages=messages,
        stream=False,
        max_tokens=500,
        temperature=0.5,
        n=1,
    )

    requestToJson = {
        "model": config["MODEL_NAME"],
        "message": messages,
        "stream": False,
        "max_token": 500,
        "temperature": "0.5",
        "n": 1,
    }

    responseToJson = {
        "id": response.id,
        "choices": [
            {
                "finish_reason": response.choices[0].finish_reason,
                "index": response.choices[0].index,
                "logprobs": response.choices[0].logprobs,
                "message": {
                    "content": response.choices[0].message.content,
                    "role": response.choices[0].message.role,
                },
            }
        ],
        "created": response.created,
        "model": response.model,
        "object": response.object,
        "system_fingerprint": response.system_fingerprint,
        "usage": {
            "completion_tokens": response.usage.completion_tokens,
            "prompt_tokens": response.usage.prompt_tokens,
            "total_tokens": response.usage.total_tokens,
        },
    }

    gptMsgArr = []
    returnData = []

    # gpt 응답 배열로 받음
    if response:
        for choice in response.choices:  # 배열 형태로 문장이 여러개 줄 가능성 있음
            gptMsgArr.append(choice.message.content)  # 한문장 출력

    tmpReturnData = []  # 리턴 데이터
    # 반복 하면서 한문장 덩어리씩 추출
    if gptMsgArr:

        totalChatTurn = totalChatTurn + 1
        curChatTurn = curChatTurn + 1

        for msg in gptMsgArr:

            msg = msg.replace(
                "<@situation>", "<@system>{show-situation}</@system><@situation>"
            )  # 메시지 replace
            msg = msg.replace(
                "<@passage>", "<@system>{show-passage}</@system><@passage>"
            )  # 메시지 replace
            msg = msg.replace(
                "<@keyword>", "<@system>{show-keyword}</@system><@keyword>"
            )  # 메시지 replace

            messageRole = "assistant"
            speaker = "AI"

            # db 입려 부분
            createHistoryData = {
                "chatId": moduleData.chatId,
                "userId": chatInfo["userId"],
                "module": moduleInfo["module"],
                "speaker": speaker,
                "message": escapeText(msg),
                "chatTurn": curChatTurn,
            }
            genHistory(createHistoryData)

            messages.append(
                {
                    "role": messageRole,
                    "content": msg,
                }
            )

            tmpData = msg.replace("\n\n", "\n")
            statementArr = tmpData.split("\n")

            print(statementArr)

            for statement in statementArr:
                splitData = extractTagsFromSentence(statement)

                for data in splitData:
                    tmpReturnData.append(data)
                    ###########################
                    # pastConversation 처리
                    ###########################
                    if data["type"] == "smallTalkSummary":
                        pastConversation = data["content"]

            returnData = workReturnData(moduleInfo["module"], tmpReturnData)

    ###########################
    # chat 업데이트
    ###########################
    setChatInfo(
        moduleData.chatId,
        escapeListMessages(messages),
        pastConversation,
        totalChatTurn,
        moduleInfo["module"],
    )

    ###########################
    # chatCompletion 등록
    ###########################
    genChatCompletion(
        chatInfo["id"],
        requestToJson,
        responseToJson,
    )

    # 디버깅용 chat.json 파일 저장
    save_state(
        filename=saveFile,
        messages=messages,
        total_chat_turn=totalChatTurn,
        cur_module_chat_turn=curChatTurn,
        current_module=moduleInfo["module"],
    )

    ###########################
    # 8. 반환
    ###########################
    return returnData
