from utility import *


# # 데이터 가공 함수
# def workReturnData(module, data):
#     if module == "E6_DIALOGUE":
#         return workDialogueData(module, data)
#     elif module == "E6_ROLEPLAYING":
#         return workRoleplayingData(module, data)
#     elif module == "E6_REVIEW_LAST_CLASS":
#         return workReviewLastClass(module, data)
#     elif module == "E6_TALK_MORE":
#         return workTalkMoreData(module, data)
#     elif module == "E6_WRAP_UP":
#         return workWrapUpData(module, data)


def genBaseFormat(module):
    return {"module": module, "answerList": [], "hintList": [], "status": "ing"}


# 다이얼로그 데이터 가공
def workReturnData(module, splitList):
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
                "translation": "",
            }

            #########################################
            # translation 추가 처리
            #########################################
            if nextData:
                if nextData["type"] == "translation":  # 다음 태그가 번역 태그일 때
                    answerData.update({"translation": nextData["content"]})

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
            curCnt = 0

            if listIndexExist(flagList, 1):
                status = "trial" if flagList[1].find("trial") >= 0 else flagList[1]
            if listIndexExist(flagList, 2):
                tmpCnt = flagList[2]
                tmpCnt = tmpCnt.split("/")
                curCnt = tmpCnt[0]
                totalCnt = tmpCnt[1]

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
                    "name": "show-passage",
                    "option": {
                        "passage": passage if passage else "",
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
