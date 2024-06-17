import datetime
import pytz


templates = {
    "initial": "./prompts/InitialSystemPrompt.jinja",
    "module1": "./prompts/PersonalizedSmallTalk.jinja",
    "module2": "./prompts/PrevSessionReview.jinja",
    "module3": "./prompts/Dialogue.jinja",
    "module4": "./prompts/Roleplaying.jinja",
    "module5": "./prompts/FreeTalk.jinja",
    "module6": "./prompts/WrapUpClose.jinja",
}
reused_prompt = {
    "recastPrompt": """
    For each of the user's message, check if it's grammatically correct and natural. If not, naturally recast the user's message to provide an IMPLICIT corrective feedback. Do not directly correct the user's mistake. If appropriate, ask a simple and short follow-up question for each response.
    """,
    "moduleMaterialGuide": """
    In the [MODULE MATERIAL], the user is provided with UI showing the sentence, potentially with some blanks. The blanks are indicated with '{}'. Do not adjust or remove the blank notation at your will; use the blank notations assigned. Also, the questions will be shown on the screen and will not be delivered verbally, so you should have the question in the <@question> QUESTION </@question> tag separately where the QUESTION is the relevant part in the [MODULE MATERIAL]. Once you output the question, there is no need to repeat it during the user's multiple trials. In some cases, Korean translation is also provided, as indicated by the sentence identifier USER_T_{set#}. Do not include or mention about the Korean translation in your spoken message. Instead, whenever the translated sentence is provided for the original English sentence, output <@translation> {USER_T_{set#}} </@translation> so that it can be displayed, along with your <@question> QUESTION </@question> message.
    """,
    "identifyNumTotalSets": """
    Identify the number of total sets as in the [MODULE MATERIAL] by checking the suffix of the sentence identifier: {USER, COACH, USER_T}_{set#}.
    """,
}
user_info = {  # Not all information is being used at the moment.
    "userName": "Yeongheon",
    "userAge": 23,
    "userGender": "Male",
    "userNationality": "Korean",
    "userCompany": "WeaversBrain",
    "userPosition": "AI Engineer",
}

kst = pytz.timezone("Asia/Seoul")
cdt = pytz.timezone("America/Chicago")

teacher_info = {
    "teacherPersona": "You are an actual human English tutor, not an AI or GPT. Your name is Linda Bailey. Below is your personal information. Female, 34 years old, Caucasian, Blonde, Green eyes, approximately 5 feet 5 inches tall, living in Springfield, Illinois Undergraduate degree, majored in Communications, have a younger sister and a younger brother, have been tutoring ESL students fo 7 years, patient, nice, eager to teach, and eager to learn.",
    "teacherTimezone": "America/Chicago",
}

other_data = {
    "currentTime": "User Timezone: "
    + str(datetime.datetime.now(kst))
    + " / Assistant Timezone: "
    + str(datetime.datetime.now(cdt)),
    "currentLocation": "User Location: South Korea",
    "pastConversation": "The user just joined a start-up, WeaversBrain as an AI Engineer during his summer vacation from University of Pennsylvania. He is currently studying computer science and cognitive science.",
    "todayExpression": "In favor of",
}

# content_info = {
#     'prevSessionReviewModuleMaterial':
#     '''
#     USER_A_1: Our team {came} {up} {with} a technical solution.
#     USER_T_1: 저희 팀이 기술적 해결 방법을 개발해냈습니다.

#     USER_A_2: {Because} {he} came up with a {better} {idea}.
#     USER_T_2: 그가 더 좋은 아이디어를 생각해냈기 때문이에요.
#     ''',
#     'dialogueModuleMaterial':
#     '''
#     USER_1: Our boss suggested adopting a new system for organizing product information.
#     COACH_1: What do you think about that idea?
#     USER_1: I am in favor of {making} a new {management} {system}.
#     USER_T_1: 저는 새로운 관리 프로그램을 만드는 것에 찬성합니다.

#     USER_2: I suggested establishing an online store to sell our products, to the CEO.
#     COACH_2: Really? What was he saying?
#     USER_2: The {CEO} {was} in favor of {selling} our products {online}.
#     USER_T_2: CEO는 우리 제품을 온라인으로 판매하는 것에 찬성했습니다.
#     '''
# }
