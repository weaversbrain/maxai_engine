import json
import re
import tiktoken

def save_state(filename, messages, **kwargs):
    with open(filename, "w") as file:
        state = {
            "messages": messages
        }
        state.update(kwargs)
        json.dump(state, file)

def load_state(filename="chat_state.json"):
    try:
        with open(filename, "r") as file:
            state = json.load(file)
        return state
    except FileNotFoundError:
        return FileNotFoundError

def str2numtoken(message_list, model_name='gpt-4-turbo'):
    if isinstance(message_list, str):
        input_str = message_list
    else:
        input_str = '\n'.join([y for message in message_list for x, y in message.items()])
    enc = tiktoken.encoding_for_model(model_name)
    num_tokens = len(enc.encode(input_str))
    return num_tokens

def token2cost(num_tokens, model_name='gpt-4-turbo', mode='input'): 
    assert mode in ('input', 'output')
    return {
        'gpt-4-turbo': (10, 30),
        'gpt-3.5-turbo': (0.5, 1.5),
        'meta-llama/Meta-Llama-3-70B-Instruct': (0.6, 0.8),
        'gpt-4o-2024-05-13': (5, 15),
        'gpt-4o': (5, 15)
    }[model_name][0 if mode == 'input' else 1] * num_tokens / (1e6)


def process_tags(text):
    system_pattern = r"(<@system>.*?</@system>)"
    hint_pattern = r"(<@hint>.*?</@hint>)"
    for tag in [
        hint_pattern,
        # system_pattern,
        ]:
        matches = re.findall(tag, text)
        for match in matches:
            text = text.replace(match, '')
    user_pattern = r"(<@user>.*?</@user>)"
    matches = re.findall(user_pattern, text)
    for match in matches:
        text = text.replace(match, match.replace('<@user>', '').replace('</@user>', ''))
    return text
