"""
+----------------------------------------------------------------------+
| Copyright (c) 2024 WeaversBrain. co. Ltd
+----------------------------------------------------------------------+
| 작업일 : 2024-05-23
| 파일설명 : 피드백
+----------------------------------------------------------------------+
| 작업자 : 박범열
+----------------------------------------------------------------------+
| 수정이력
|
+----------------------------------------------------------------------+ 
"""

from litellm import completion
from openai import OpenAI
from dotenv import load_dotenv
from model import CreateFeedbackModel
from crud import *
from utility import *
from dotenv import dotenv_values
from prompt_base import templates
import os
import json
import time

# 절대경로
abspath = os.path.dirname(os.path.abspath(__file__))
config = dotenv_values(abspath + "/.env")  # 환경변수 읽어오기

# set ENV variables
os.environ["OPENAI_API_KEY"] = config["API_KEY1"]


def createFeedback(createFeedbackModel):

    totalStartTime = time.time()

    #########################################
    # set LLM options
    #########################################
    MODEL = config["MODEL_NAME"]
    STREAM = False
    MAX_TOKEN = 4096
    TEMPERATURE = 0.5
    NUM = 1

    #########################################
    # init variables
    #########################################
    renderData = {}
    messages = []

    #########################################
    # chat Info 추출
    #########################################
    chatInfo = getChat(createFeedbackModel.chatId)

    if not chatInfo:
        return {"code": "E", "msg": "채팅 정보가 없습니다."}

    renderData.update(chatInfo)
    #########################################
    # 자유 발화가 포함된 모듈의 대화내역 추출
    #########################################
    historyData = {}
    historyData["chatId"] = createFeedbackModel.chatId
    historyData["userId"] = createFeedbackModel.userId
    historyData["inModule"] = ["E6_SMALL_TALK", "E6_ROLEPLAYING", "E6_TALK_MORE"]

    historyList = getListHistory(historyData)

    #########################################
    # 대화내역 가공
    #########################################
    chatHistory = []
    for history in historyList:
        speaker = history["speaker"]
        msg = history["message"]

        if speaker == "USER":
            chatHistory.append(
                {"chatStatementId": history["id"], "type": "USER", "message": msg}
            )
        else:
            tmpData = msg.replace("\n\n", "\n")
            statementArr = tmpData.split("\n")

            for statement in statementArr:
                splitData = extractTagsFromSentence(statement)

                for data in splitData:
                    if data["type"] == "user":
                        chatHistory.append(
                            {
                                "chatStatementId": history["id"],
                                "type": "AI",
                                "message": data["content"],
                            }
                        )

    renderData.update({"messageList": chatHistory})

    renderedStr = renderTemplate("FEEDBACK", renderData)

    messageData = {
        "role": "system",
        "content": renderedStr,
    }
    messages.append(messageData)

    #########################################
    # LLM 처리
    #########################################
    llmStartTime = time.time()
    response = completion(
        model=MODEL,
        messages=messages,
        stream=STREAM,
        max_tokens=MAX_TOKEN,
        temperature=TEMPERATURE,
        n=NUM,
    )
    llmEndTime = time.time()
    llmTime = llmEndTime - llmStartTime

    ###########################
    # chatCompletion 등록
    ###########################
    # 요청 데이터 내용
    requestToJson = {
        "model": MODEL,
        "message": messages,
        "stream": STREAM,
        "max_token": MAX_TOKEN,
        "temperature": TEMPERATURE,
        "n": NUM,
    }

    # 응답 데이터 내용
    responseToJson = {
        "id": response.id,
        "choices": [
            {
                "finish_reason": response.choices[0].finish_reason,
                "index": response.choices[0].index,
                "message": {
                    "content": response.choices[0].message.content,
                    "role": response.choices[0].message.role,
                },
            }
        ],
        "created": response.created,
        "model": response.model,
        "usage": {
            "completion_tokens": response.usage.completion_tokens,
            "prompt_tokens": response.usage.prompt_tokens,
            "total_tokens": response.usage.total_tokens,
        },
    }

    # token 개수 구함
    inputTokens = getTokenNums(messages)
    outputTokens = getTokenNums(response.choices[0].message.content)

    # 토큰 비용 계산
    inputCost = getTokenCost(inputTokens, MODEL, "input")
    outputCost = getTokenCost(outputTokens, MODEL, "output")

    #########################################
    # 데이터 가공
    #########################################
    feedbackData = response.choices[0].message.content
    feedbackData = json.loads(feedbackData.replace("json", "").replace("```", ""))

    tutorComment = feedbackData["tutorComment"]
    thingsToImprove = feedbackData["thingsToImprove"]

    #########################################
    # DB처리
    #########################################
    updateData = {
        "tutorComment": tutorComment,
        "thingsToImprove": json.dumps(thingsToImprove, ensure_ascii=False),
    }

    whereData = {"id": createFeedbackModel.chatId}

    setChat(
        updateData,
        whereData,
    )

    totalEndTime = time.time()  # 전체 종료 시간
    totalTime = totalEndTime - totalStartTime

    ###########################
    # chatCompletion 등록
    ###########################
    completionData = {
        "chatId": chatInfo["id"],
        "request": requestToJson,
        "response": responseToJson,
        "inputTokens": inputTokens,
        "outputTokens": outputTokens,
        "inputCost": inputCost,
        "outputCost": outputCost,
        "llmTime": llmTime,
        "totalTime": totalTime,
    }

    genChatCompletion(completionData)

    return {"code": "Y", "msg": "성공"}
