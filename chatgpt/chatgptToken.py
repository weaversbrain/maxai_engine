import tiktoken

# chatGPT 토큰값 계산
tokenizer = tiktoken.get_encoding("cl100k_base")
tokenizer = tiktoken.encoding_for_model("gpt-3.5-turbo") # "gpt-4"도 가능

text = "안녕하세요. 반갑습니다!"

tokenizer.encode(text) # [31495, 230, 75265, 243, 92245, 13, 64857, 14705, 239, 39331, 0]

encoding_result = tokenizer.encode(text)

print(len(encoding_result)) # 11

encode_result = [31495, 230, 75265, 243, 92245, 13, 64857, 14705, 239, 39331, 0]

tokenizer.decode(encode_result) # '안녕하세요. 반갑습니다!'

encode_result = tokenizer.encode(text)[:6]

print(tokenizer.decode(encode_result)) # '안녕하세요.'