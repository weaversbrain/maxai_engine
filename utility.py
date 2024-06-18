import jinja2
from prompt_base import templates
from openai import OpenAI
import re
import os
from dotenv import load_dotenv
import json
import tiktoken


def renderTemplate(module: str, data: dict):
    templateEnvironment = jinja2.Environment(
        loader=jinja2.FileSystemLoader(searchpath="./")
    )
    renderedTemplate = templateEnvironment.get_template(templates[module]).render(data)

    return renderedTemplate


load_dotenv()  # 환경변수 읽어오기

STREAM = False
openaiClient = OpenAI(
    api_key=os.getenv("API_KEY1"),
)


# chatGPT
def getChatGptResponse(messages, model_name="gpt-4o-2024-05-13"):
    response = openaiClient.chat.completions.create(
        model=model_name,
        messages=messages,
        stream=STREAM,
        max_tokens=200,
        temperature=0.5,
    )
    return response.choices[0].message.content.strip()


# HTML tab 제거
def cleanHtml(rawHtml):
    cleanRex = re.compile("<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});")
    cleanText = re.sub(cleanRex, "", rawHtml)
    return cleanText


# def extractTags(string: str):
#     pattern = r"<@(system|hint|user|assistant|question|translation)>(.*?)<\/@\1>"
#     matches = re.findall(pattern, string)
#     tag_info = []
#     for match in matches:
#         tag_info.append(
#             {
#                 "type": match[0],
#                 "content": match[1],
#                 "message": f"<@{match[0]}>{match[1]}</@{match[0]}>",
#             }
#         )
#     return tag_info


def extractTags(data):
    # 정규 표현식 패턴
    pattern = r"<@(.*?)(:\{(.*?)\})?>(.*?)</@(.*?)(:\{(.*?)\})?[}>]*>"

    # 데이터에서 패턴에 맞는 모든 부분을 찾아 리스트로 반환
    matches = re.findall(pattern, data, re.DOTALL)

    returnData = []
    for match in matches:
        openTagType = match[0].strip()
        openTagFlag = match[2].split(",") if match[2] else []
        content = match[3].strip()

        closeTagType = match[4].strip()
        closeTagFlag = match[6].split(",") if match[6] else []

        findData = {
            "type": openTagType,
            "content": content,
        }

        # {}에 포함된 내용 추가
        if openTagFlag:
            findData["prevFlag"] = openTagFlag
        if closeTagFlag:
            findData["nextFlag"] = closeTagFlag

        returnData.append(findData)

    return returnData


def extractTagsFromSentence(sentence):
    all_tags = []
    tags_in_sentence = extractTags(sentence)
    all_tags.extend(tags_in_sentence)

    return all_tags


def escapeText(text):
    return text.replace("'", "\\'").replace('"', '\\"')


def escapeListMessages(messages):
    escapedMessages = []
    if messages:
        for message in messages:
            tmpDict = {
                "role": message["role"],
                "content": message["content"]
                .replace("'", "\\'")
                .replace('"', '\\"')
                .replace("\n", ""),
            }
            escapedMessages.append(tmpDict)

    return escapedMessages


def extractBraces(string):
    flags = []
    start_index = 0
    for i, char in enumerate(string):
        if char == "{":
            start_index = i
        elif char == "}":
            flag = string[start_index + 1 : i]
            if flag:
                flags.append(flag)
    if not flags:
        return [string]  # 빈 배열일 때 문자열 자체를 반환합니다.
    return flags


def save_state(filename, messages, **kwargs):
    with open(filename, "w") as file:
        state = {"messages": messages}
        state.update(kwargs)
        json.dump(state, file)


def load_state(filename="chat_state.json"):
    try:
        with open(filename, "r") as file:
            state = json.load(file)
        return state
    except FileNotFoundError:
        return FileNotFoundError


def str2numtoken(message_list, model_name="gpt-4-turbo"):
    if isinstance(message_list, str):
        input_str = message_list
    else:
        input_str = "\n".join(
            [y for message in message_list for x, y in message.items()]
        )
    enc = tiktoken.encoding_for_model(model_name)
    num_tokens = len(enc.encode(input_str))
    return num_tokens


def token2cost(num_tokens, model_name="gpt-4-turbo", mode="input"):
    assert mode in ("input", "output")
    return (
        {
            "gpt-4-turbo": (10, 30),
            "gpt-3.5-turbo": (0.5, 1.5),
            "meta-llama/Meta-Llama-3-70B-Instruct": (0.6, 0.8),
            "gpt-4o-2024-05-13": (5, 15),
            "gpt-4o": (5, 15),
        }[model_name][0 if mode == "input" else 1]
        * num_tokens
        / (1e6)
    )


def process_tags(text):
    system_pattern = r"(<@system>.*?</@system>)"
    hint_pattern = r"(<@hint>.*?</@hint>)"
    for tag in [
        hint_pattern,
        # system_pattern,
    ]:
        matches = re.findall(tag, text)
        for match in matches:
            text = text.replace(match, "")
    user_pattern = r"(<@user>.*?</@user>)"
    matches = re.findall(user_pattern, text)
    for match in matches:
        text = text.replace(match, match.replace("<@user>", "").replace("</@user>", ""))
    return text


def formatResponseData(msg):
    returnData = []
    tmpData = msg.replace("\n\n", "\n")
    statementArr = tmpData.split("\n")

    for statement in statementArr:
        splitData = extractTags(statement)
        returnData.extend(splitData)

    return returnData


# 빈칸 위치 찾기
def findBlanksIndex(sentence):
    words = sentence.split()
    indices = []

    current_index = 0

    while True:
        start_index = sentence.find("{", current_index)
        end_index = sentence.find("}", start_index)

        if start_index == -1 or end_index == -1:
            break

        # Find the word index where { starts
        word_index = len(sentence[:start_index].split())

        # Add to indices
        indices.append(word_index)

        # Move current_index past the }
        current_index = end_index + 1

    return indices


# 인덱스 존재 여부 파악
def listIndexExist(arr, i):
    return (0 <= i < len(arr)) or (-len(arr) <= i < 0)


# {}를 제거하여 텍스트만 추출
def removeBraces(text):
    result = text.replace("{", "").replace("}", "")
    return result
