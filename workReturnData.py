from litellm import completion
from dotenv import load_dotenv
from utility import *
from dotenv import dotenv_values
from crud import *
import os

# 절대경로
abspath = os.path.dirname(os.path.abspath(__file__))
config = dotenv_values(abspath + "/.env")  # 환경변수 읽어오기

# set ENV variables
os.environ["OPENAI_API_KEY"] = config["API_KEY1"]


def genBaseFormat(module):
    return {"module": module, "answerList": [], "hintList": [], "status": "ing"}


def getTranslation(chatId, text):
    prompt = f"Translate the following sentence into Korean: <Sentence to Translate>{text}</Sentence to Translate>"

    messages = []
    messages.append({"role": "assistant", "content": text})
    messages.append({"role": "system", "content": prompt})

    response = completion(
        model=config["MODEL_NAME"],
        messages=messages,
        stream=False,
        max_tokens=500,
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
        "max_token": 500,
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

    genChatCompletion(
        chatId,
        requestToJson,
        responseToJson,
    )

    return cleanHtml(response.choices[0].message.content).strip()


# 다이얼로그 데이터 가공
def workReturnData(chatId, module, splitList):
    if not chatId or not module or not splitList:
        return None

    hintList = []

    baseFormat = genBaseFormat(module)

    #########################################
    # 응답 리스트 반복
    #########################################
    for i, data in enumerate(splitList):
        answerData = {}
        nextData = ""

        if listIndexExist(splitList, i + 1):
            nextData = splitList[i + 1]

        #########################################
        # user 타입 처리
        #########################################
        if data["type"] == "user":

            answerData = {
                "type": "user",
                "speaker": "AI",
                "content": data["content"],
                "translation": getTranslation(chatId, data["content"]),
            }

            #########################################
            # translation 추가 처리
            #########################################
            # if nextData:
            #     if nextData["type"] == "translation":  # 다음 태그가 번역 태그일 때
            #         answerData.update({"translation": nextData["content"]})

            baseFormat["answerList"].append(answerData)

        #########################################
        # system 타입 처리
        #########################################
        elif data["type"] == "system":
            #########################################
            # flag, status, cnt 할당
            #########################################
            flagList = extractBraces(data["content"])

            flag = flagList[0]
            status = ""
            totalCnt = 0
            curIdx = 0

            if listIndexExist(flagList, 1):
                status = "trial" if flagList[1].find("trial") >= 0 else flagList[1]
            if listIndexExist(flagList, 2):
                tmpCnt = flagList[2]
                tmpCnt = tmpCnt.split("/")
                curIdx = int(tmpCnt[0]) - 1 if int(tmpCnt[0]) > 0 else 0
                totalCnt = int(tmpCnt[1])

            #########################################
            # 로직 처리
            #########################################
            if flag == "fill-in-the-blank":
                question = ""
                translation = ""
                blankIdxArr = []

                if nextData:
                    for j in range(i + 1, len(splitList)):
                        splitData = splitList[j]
                        if splitData["type"] == "user" or splitData["type"] == "system":
                            break

                        if splitData["type"] == "question":
                            question = splitData["content"]
                            blankIdxArr = findBlanksIndex(question)
                        elif splitData["type"] == "translation":
                            translation = splitData["content"]

                answerData = {
                    "type": "system",
                    "name": "fill-in-the-blank",
                    "option": {
                        "status": status if status else "",
                        "totalCnt": totalCnt if totalCnt else "",
                        "curIdx": curIdx if curIdx else 0,
                        "blankBoxList": [
                            {
                                "firstRole": "AI",
                                "content": removeBraces(question) if question else "",
                                "blankIdxArr": (
                                    blankIdxArr if len(blankIdxArr) > 0 else []
                                ),
                                "translation": translation if translation else "",
                            },
                        ],
                    },
                }

                baseFormat["answerList"].append(answerData)

            elif flag == "copy-read":
                question = ""

                if nextData:
                    for j in range(i + 1, len(splitList)):
                        splitData = splitList[j]
                        if splitData["type"] == "user" or splitData["type"] == "system":
                            break

                        if splitData["type"] == "question":
                            question = splitData["content"]

                answerData = {
                    "type": "system",
                    "name": "copy-read",
                    "option": {
                        "status": status if status else "",
                        "totalCnt": totalCnt if totalCnt else "",
                        "curIdx": curIdx if curIdx else 0,
                        "dialogue": [
                            {
                                "content": question if question else "",
                                "speaker": "USER",
                            },
                        ],
                    },
                }

                baseFormat["answerList"].append(answerData)

            elif flag == "show-situation":
                situation = ""

                if nextData:
                    for j in range(i + 1, len(splitList)):
                        splitData = splitList[j]
                        if splitData["type"] == "user" or splitData["type"] == "system":
                            break

                        if splitData["type"] == "situation":
                            situation = splitData["content"]

                answerData = {
                    "type": "system",
                    "name": "show-situation",
                    "option": {
                        "situation": situation if situation else "",
                    },
                }

                baseFormat["answerList"].append(answerData)

            elif flag == "show-passage":
                passage = ""

                if nextData:
                    for j in range(i + 1, len(splitList)):
                        splitData = splitList[j]
                        if splitData["type"] == "user" or splitData["type"] == "system":
                            break

                        if splitData["type"] == "passage":
                            passage = splitData["content"]

                answerData = {
                    "type": "system",
                    "name": flag,
                    "option": {
                        "passage": passage if passage else "",
                    },
                }

                baseFormat["answerList"].append(answerData)

            elif flag == "show-keyword":
                keyword = ""

                if nextData:
                    for j in range(i + 1, len(splitList)):
                        splitData = splitList[j]
                        if splitData["type"] == "user" or splitData["type"] == "system":
                            break

                        if splitData["type"] == "keyword":
                            keyword = splitData["content"]

                answerData = {
                    "type": "system",
                    "name": flag,
                    "option": {
                        "keyword": keyword if keyword else "",
                    },
                }

                baseFormat["answerList"].append(answerData)

            elif flag == "open-answer":
                answerData = {
                    "type": "system",
                    "name": flag,
                    "option": {
                        "status": status if status else "",
                        "totalCnt": totalCnt if totalCnt else "",
                        "curIdx": curIdx if curIdx else 0,
                    },
                }

                baseFormat["answerList"].append(answerData)

            else:
                answerData = {
                    "type": "system",
                    "name": flag,
                    "option": {},
                }

                if flag == "module-transition" or flag.find("ModuleTransition") >= 0:
                    baseFormat["status"] = "end"

                baseFormat["answerList"].append(answerData)

        elif data["type"] == "hint":
            hintList.append(data["content"])

    #########################################
    # 힌트, 모듈 상태값 추가
    #########################################
    baseFormat["hintList"] = hintList

    return baseFormat
