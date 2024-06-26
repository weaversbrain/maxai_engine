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

from litellm import completion
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
from workReturnData import *

# 절대경로
abspath = os.path.dirname(os.path.abspath(__file__))
config = dotenv_values(abspath + "/.env")  # 환경변수 읽어오기

# set ENV variables
os.environ["OPENAI_API_KEY"] = config["API_KEY1"]


def runEngin6(moduleData: ModuleModel, type: str):

    totalStartTime = time.time()  # 전체 로직 시작 시간

    #########################################
    # set LLM options
    #########################################
    MODEL = config["MODEL_NAME"]
    STREAM = False
    MAX_TOKEN = 500
    TEMPERATURE = 0.5
    NUM = 1

    ###########################
    # 초기 세팅
    ###########################
    renderData = {}
    messages = []
    totalChatTurn = 0
    pastConversation = ""
    userChatStatementId = 0

    # saveFile = f"log/chat_{moduleData.chatId}.json"  # 로그 파일

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
    
    #########################################
    # 프롬프트 추출
    #########################################
    promptList = getPromptList()
    renderDict = {}
    
    if not promptList:
        return {"code": "E", "msg": "프롬프트 데이터가 없습니다."}
    
    for prompt in promptList:
        renderDict.update(
            {
                prompt['name']: prompt['content']
            }
        )
    

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
    # pastConversation 추출
    ###########################
    if moduleInfo["module"] == "E6_SMALL_TALK":
        lastChat = getLastChat(chatInfo["id"], chatInfo["userId"])

        if lastChat and lastChat["pastConversation"]:
            renderData.update({"pastConversation": lastChat["pastConversation"]})
            renderData.update({"pastConversationTime": lastChat["updatedAt"]})

    ###########################
    # 2. initialize 작업
    ###########################
    # renderedStr = renderTemplate("INITIAL", renderData)
    renderedStr = renderPrompt(renderDict['E6_INITIAL'], renderData)
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
    renderedStr = renderPrompt(renderDict[moduleInfo['module']], renderData)
    # renderedStr = renderTemplate(moduleInfo["module"], renderData)

    messageData = {
        "role": "system",
        "content": renderedStr,
    }
    messages.append(messageData)

    if totalChatTurn == 0:
        createHistoryData = {
            "chatId": moduleData.chatId,
            "userId": chatInfo["userId"],
            "module": moduleInfo["module"],
            "speaker": "USER",
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
    # USER Answer 처리
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
            "message": moduleData.userAnswer,
            "chatTurn": curChatTurn,
        }

        userChatStatementId = genHistory(createHistoryData)

    ###########################
    # LLM 처리
    ###########################
    messages.append({"role": "system", "content": f"ChatTurn: {curChatTurn}"})
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

    requestToJson = {
        "model": MODEL,
        "message": messages,
        "stream": STREAM,
        "max_token": MAX_TOKEN,
        "temperature": TEMPERATURE,
        "n": NUM,
    }

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
                "message": msg,
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

            for statement in statementArr:
                splitData = extractTagsFromSentence(statement)

                for data in splitData:
                    tmpReturnData.append(data)
                    ###########################
                    # pastConversation 처리
                    ###########################
                    if data["type"] == "smallTalkSummary":
                        pastConversation = data["content"]

            workedData = workReturnData(
                chatInfo["id"], moduleInfo["module"], tmpReturnData
            )

            if not workedData:
                return {"code": "E", "msg": "데이터 가공 필수값 누락"}

            returnData = workedData

    totalEndTime = time.time()  # 전체 로직 종료 시간
    totalTime = totalEndTime - totalStartTime

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
    completionData = {
        "chatId": chatInfo["id"],
        "request": requestToJson,
        "response": responseToJson,
        "returnData": returnData,
        "inputTokens": inputTokens,
        "outputTokens": outputTokens,
        "inputCost": inputCost,
        "outputCost": outputCost,
        "llmTime": llmTime,
        "totalTime": totalTime,
    }

    genChatCompletion(completionData)

    # 디버깅용 chat.json 파일 저장
    # save_state(
    #     filename=saveFile,
    #     messages=messages,
    #     total_chat_turn=totalChatTurn,
    #     cur_module_chat_turn=curChatTurn,
    #     current_module=moduleInfo["module"],
    # )

    ###########################
    # 8. 반환
    ###########################
    return {"responseData": returnData, "userChatStatementId": userChatStatementId}
