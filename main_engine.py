import jinja2
import pandas as pd
import time
import numpy as np
import json
from prompt_base import other_data, reused_prompt, teacher_info, templates, user_info
from utils import process_tags, save_state, load_state, str2numtoken, token2cost
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv() # 환경변수 읽어오기goo

# Set up your OpenAI API key
# MODEL_NAME = 'gpt-3.5-turbo'
# MODEL_NAME = "meta-llama/Meta-Llama-3-70B-Instruct"
MODEL_NAME = "gpt-4o-2024-05-13"
# MODEL_NAME = "gpt-4-turbo"

if MODEL_NAME.startswith('gpt'):
    openai = OpenAI(
        api_key=os.getenv('API_KEY1'),
        # base_url="https://api.openai.com/v1",
    )
else:
    openai = OpenAI(
        api_key=os.getenv('API_KEY2'),
        base_url="https://api.deepinfra.com/v1/openai",
    )

if __name__ == '__main__':
    # Path to the template file
    data = {}
    data.update(other_data)
    data.update(teacher_info)
    data.update(user_info)
    data.update(reused_prompt)
    
    # Render the template with the data
    template_environment = jinja2.Environment(loader=jinja2.FileSystemLoader(searchpath='./'))
    initial_rendered = template_environment.get_template(templates['initial']).render(data)
    prompt_dict = {x: template_environment.get_template(y).render(data) for x, y in templates.items()}
    
    STREAM = True
    USE_SAVED_STATE = False
    AUTO_GENERATE = False
    REMOVE_PREV_MODULE_PROMPT = True
    save_file = 'chat_state.json'
    reload_last_module_prompt = None
    chat_state_log = {}
    log_list = []
    
    if USE_SAVED_STATE:
        loaded_state = load_state(save_file)
        messages, chat_turn, current_module = loaded_state['messages'], loaded_state['chat_turn'], loaded_state['current_module']
        reload_last_module_prompt = True
        if reload_last_module_prompt:
            messages[-1] = {'role': 'system', 'content': prompt_dict['module{}'.format(current_module)]}
    else:
        messages = [
            {"role": "system", "content": prompt_dict['initial']},
            {"role": "system", "content": prompt_dict['module1']},
            {"role": "user", "content": "(entered classroom)"}
        ]
        chat_turn = 0
        module_index = 1
    
    while True:
        # GENERATE AI RESPONSE
        messages.append({"role": "system", "content": "ChatTurn: {}".format(chat_turn)})
        start_time = time.time()
        
        print(messages)
        response = openai.chat.completions.create(
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
    
        # CALL BACK ACTIONS
        if 'ModuleTransition' in gpt_response:
            # Add current module index.
            module_index += 1
            if module_index == 7:
                break
            # Clear previous system prompts.
            if REMOVE_PREV_MODULE_PROMPT:
                # Remove previous system prompt modules except for the initial prompt and the new module prompt.
                messages = [x for x in messages if x['role'] != 'system']
                # Remove previous messages @hint for prompt compression.
                # messages = [{'role': x['role'], 'content': process_tags(x['content'])} for x in messages]
                messages.insert(0, {'role': 'system', 'content': prompt_dict['initial']})
    
            # Inject module prompt.
            messages.append(
                {'role': 'system', 'content': prompt_dict['module{}'.format(module_index)]})
            messages.append(
                {'role': 'system', 'content': 'CurrentTime: {}'.format(time.strftime('%H:%M:%S'))})
            
            # messages.append({'role': 'user', 'content': 'okay'})
            # Reset chat turn.
            chat_turn = 0
            save_state(filename=save_file, messages=messages, 
                       chat_turn=chat_turn, current_module=module_index)
        else:
            if AUTO_GENERATE and '<@hint>' in gpt_response:
                user_response = gpt_response.split('<@hint>')[1].split('</@hint>')[0]
                messages.append({"role": "user", "content": gpt_response.split('<@hint>')[1].split('</@hint>')[0]})
                print("\nUser: ", user_response)
            else:
                user_response = input("\nUser: ")
                if user_response.lower() in ['exit', 'quit']:
                    print("Chat ended.")
                    break
                if user_response == '':
                    user_response = '(said nothing - maybe due to bad internet connection)'
                messages.append({"role": "user", "content": user_response})
            chat_turn += 1
    
        # LOGGING
        chat_state_log['ChatTurn'] = chat_turn
        chat_state_log['Module'] = templates['module{}'.format(module_index)].split('/')[-1].split('.')[0]
        chat_state_log['Time2FirstToken'] = first_token_time
        chat_state_log['Time2LastToken'] = last_token_time
        chat_state_log['InputTokens'] = str2numtoken(messages[:-1])
        chat_state_log['InputCost'] = token2cost(chat_state_log['InputTokens'], model_name=MODEL_NAME, mode='input')
        chat_state_log['OutputCost'] = token2cost(str2numtoken(
            messages[-1]['content']), model_name=MODEL_NAME, mode='output')
        chat_state_log['Context'] = '\n'.join([x + ': ' + y for message in messages for x, y in message.items()])
        chat_state_log['Message_AI'] = gpt_response
        chat_state_log['Message_User'] = user_response
        log_list.append(pd.Series(chat_state_log))
        pd.DataFrame(log_list).to_excel('chat_log_{}.xlsx'.format(data['currentTime'].split('.')[0].replace(':', '-')), index=False)