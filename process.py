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
# from utility import renderTemplate
from openai import OpenAI
import datetime, os
from dotenv import load_dotenv
from model import CreateChatModel, ModuleModel
from crud import *
from utility import *
import sys
import time
import pytz
import jinja2
import json


templates = {
    'initial': './prompts/InitialSystemPrompt.jinja',
    'module1': './prompts/PersonalizedSmallTalk.jinja',
    'module2': './prompts/PrevSessionReview.jinja',
    'module3': './prompts/Dialogue.jinja',
    'module4': './prompts/Roleplaying.jinja',
    'module5': './prompts/FreeTalk.jinja',
    'module6': './prompts/WrapUpClose.jinja'
}

def runEngin6(moduleData: ModuleModel):

    renderData = {}

    ######################################
    # 유저 정보 세팅
    ######################################


    chatId = int(moduleData['chatId'])    # chat id
    #current_module = data['module'] # 현재 모듈

    fakeData = {"chatId": chatId}

    chatData = getChat(fakeData) # chat table 데이터 가져오기

    userInfo = {'userName': chatData['userName'], 'userNationality': 'Korean'}

    ######################################
    # 튜터 정보 세팅
    ######################################

    tutorInfo = {'teacherPersona': chatData['teacherPersona'], 'teacherTimezone': 'America/Chicago'}


    ######################################
    # 기타 필요 정보 세팅
    ######################################

    # pastConversation 가져오기
    pastConversation = "The user just joined a start-up, StudyMax."
    #pastConversation = ""    
    todayExpression = "well known for"

    kst = pytz.timezone('Asia/Seoul')
    cdt = pytz.timezone('America/Chicago')

    otherInfo = {
        "currentTime": "User Timezone: "
        + str(datetime.datetime.now(kst))
        + " / Assistant Timezone: "
        + str(datetime.datetime.now(cdt)),
        "currentLocation": "User Location: South Korea",
        "pastConversation": pastConversation,
        "todayExpression": todayExpression,
    }

    renderData.update(userInfo)
    renderData.update(tutorInfo)
    renderData.update(otherInfo)

    # 모듈이 initial인 경우
    
    # Render the template with the data
    template_environment = jinja2.Environment(loader=jinja2.FileSystemLoader(searchpath='./'))
    initial_rendered = template_environment.get_template(templates['initial']).render(renderData)
    prompt_dict = {x: template_environment.get_template(y).render(renderData) for x, y in templates.items()}

    if(moduleData['module'] == 'initial') :

        USE_SAVED_STATE = False
        AUTO_GENERATE = False
        REMOVE_PREV_MODULE_PROMPT = True
        save_file = 'chat_state.json'
        reload_last_module_prompt = None
        chat_state_log = {}
        log_list = []

        messages = [
            {"role": "system", "content": prompt_dict['initial']},
            {"role": "system", "content": prompt_dict['module1']},
            {"role": "user", "content": "(entered classroom)"}
        ]
        chat_turn = 0
        module_index = 1

        messages.append({"role": "system", "content": "ChatTurn: {}".format(chat_turn)})
        response = getChatGptResponse(messages)
        messages.append({"role": "assistant", "content": response})
        
        updateChatStatement(chatId,messages,chat_turn,module_index)
        return response

    else:
        #print(loaded_state)
        #return
        #loaded_state = json.loads(chatData.chatState)

        messages, chat_turn, current_module = json.loads(str(chatData['messages']), strict=False), int(chatData['chatTurn']), int(chatData['currentModule'])
        
        messages[-1] = {'role': 'system', 'content': prompt_dict['module{}'.format(current_module)]}

        user_response = moduleData['userMessage'] #data.userMessage
        messages.append({"role": "user", "content": user_response})
        if user_response.lower() in ['exit', 'quit']:
            updateChatStatement(chatId,messages)  
            return

        if user_response == '':
            user_response = '(said nothing - maybe due to bad internet connection)'
        messages.append({"role": "user", "content": user_response})
        chat_turn += 1

        response = getChatGptResponse(messages)
        messages.append({"role": "assistant", "content": response})

        updateChatStatement(chatId,messages,chat_turn,current_module)
        return response



    """
    # CALL BACK ACTIONS
    if 'ModuleTransition' in gpt_response:
        # Add current module index.
        module_index += 1
        if module_index == 7:
            return

        # Clear previous system prompts.
        if REMOVE_PREV_MODULE_PROMPT:
            # Remove previous system prompt modules except for the initial prompt and the new module prompt.
            messages = [x for x in messages if x['role'] != 'system']
            # Remove previous messages @hint for prompt compression.
            # messages = [{'role': x['role'], 'content': process_tags(x['content'])} for x in messages]
            messages.insert(0, {'role': 'system', 'content': prompt_dict['initial']})

        # Inject module prompt.        messages.append(
            {'role': 'system', 'content': prompt_dict['module{}'.format(module_index)]})
        messages.append(
            {'role': 'system', 'content': 'CurrentTime: {}'.format(time.strftime('%H:%M:%S'))})
        
        # messages.append({'role': 'user', 'content': 'okay'})
        # Reset chat turn.
        chat_turn = 0


        # chat chatState 에 저장하기  
        #save_state(filename=save_file, messages=messages, chat_turn=chat_turn, current_module=module_index)

    else:
        if AUTO_GENERATE and '<@hint>' in gpt_response:
            user_response = gpt_response.split('<@hint>')[1].split('</@hint>')[0]
            messages.append({"role": "user", "content": gpt_response.split('<@hint>')[1].split('</@hint>')[0]})
            print("\nUser: ", user_response)
        else:
            #user_response = input("\nUser: ")
            user_response = data.answer

            if user_response.lower() in ['exit', 'quit']:
                print("Chat ended.")
                return
            if user_response == '':
                user_response = '(said nothing - maybe due to bad internet connection)'
            messages.append({"role": "user", "content": user_response})
        chat_turn += 1
    """




