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

from openai import OpenAI
from dotenv import load_dotenv
from model import CreateFeedbackModel
from crud import *
from utility import *
from dotenv import dotenv_values
from prompt_base import templates
import os
import json

# 절대경로
abspath = os.path.dirname(os.path.abspath(__file__))
config = dotenv_values(abspath + "/.env")  # 환경변수 읽어오기


def createFeedback(createFeedbackModel):

    renderData = {}
    messages = []

    if config["MODEL_NAME"].startswith("gpt"):
        openai = OpenAI(
            api_key=config["API_KEY1"],
        )
    else:
        openai = OpenAI(
            api_key=config["API_KEY2"],
            base_url="https://api.deepinfra.com/v1/openai",
        )

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
    response = openai.chat.completions.create(
        model=config["MODEL_NAME"],
        messages=messages,
        stream=False,
        max_tokens=4096,
        temperature=0.5,
        n=1,
    )

    ###########################
    # chatCompletion 등록
    ###########################
    # 요청 데이터 내용
    requestToJson = {
        "model": config["MODEL_NAME"],
        "message": messages,
        "stream": False,
        "max_token": 4096,
        "temperature": 0.5,
        "n": 1,
    }

    # 응답 데이터 내용
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

    genChatCompletion(
        chatInfo["id"],
        requestToJson,
        responseToJson,
    )

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
        "tutorComment": escapeText(tutorComment),
        "thingsToImprove": escapeText(json.dumps(thingsToImprove, ensure_ascii=False)),
    }

    whereData = {"id": createFeedbackModel.chatId}

    setChat(
        updateData,
        whereData,
    )

    return {"code": "Y", "msg": "성공"}
