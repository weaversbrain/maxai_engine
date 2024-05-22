from openai import OpenAI
import re
import os
from dotenv import load_dotenv

load_dotenv() # 환경변수 읽어오기

client = OpenAI(
    api_key=os.getenv('CHATGPT_API_KEY') # chatGPT API KEY
)

# chatGPT 번역
def chat_gpt(text):    
    translation_system_prompt = "Based on the conversation, translate the assistant's LAST MESSAGE into Korean, for the user who is having a video conference style tutoring session with the assistant. The user's English proficiency is beginner \n The purpose of this translation is to help the user to better follow the assistant's tutoring, since the medium of instruction is English. Therefore, some parts should be left as English: \n (1) Do not translate standard English proper nouns like names into Korean. For example, if the user name is YoungChan or 영찬, keep it as YoungChan. \n (2) Do not translate English learning material that is supposed to remain in English: For example, when the student is asked to repeat an English sentence, it'd be better to translate the instruction part only; \'Repeat after me: I like apples.\' should be translated into \'따라말해 보세요: I like apples.\' \n To make the translation sound gentle and friendly, try to use style that finishes with \'요.\' or \'요?\'. As another example, prefer using \'했어요\' to using \'했습니다\'. For \'해봅시다', you can use \'해볼게요\'. \n\n Begin your response with <translation> tag and close it with </translation> tag. Do not include anything else, except for the translation."
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "assistant", "content": text},{"role": "system", "content": translation_system_prompt}]
    )
    return response.choices[0].message.content.strip()

# HTML tab 제거
def cleanhtml(raw_html):
  cleanr = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
  cleantext = re.sub(cleanr, '', raw_html)
  return cleantext

print(cleanhtml(chat_gpt("I am a boy")))