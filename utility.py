import jinja2
from prompt_base import templates
from openai import OpenAI
import re
import os
from dotenv import load_dotenv


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


"""
def getChatGptResponse(messages):
    # GENERATE AI RESPONSE
    messages.append({"role": "system", "content": "ChatTurn: {}".format(chat_turn)})
    start_time = time.time()
    response = openaiClient.chat.completions.create(
        model=MODEL_NAME, messages=messages, stream=STREAM, max_tokens=200, temperature=0.5)

    first_token_time = time.time() - start_time
    collected_messages = []
    print("\nAI:")

    for chunk in response:
        chunk_message = chunk.choices[0].delta.content
        if chunk_message is None:
            last_token_time = time.time() - start_time
            break
        print(chunk_message, end = "", flush=True)
        collected_messages.append(chunk_message)
    gpt_response = ''.join(collected_messages)
    messages.append({"role": "assistant", "content": gpt_response})
"""


# HTML tab 제거
def cleanhtml(raw_html):
    cleanr = re.compile("<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});")
    cleantext = re.sub(cleanr, "", raw_html)
    return cleantext
