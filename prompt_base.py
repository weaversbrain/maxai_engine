import datetime
import pytz

templates = {
    "INITIAL": "./prompts/InitialSystemPrompt.jinja",
    "SMALL_TALK": "./prompts/PersonalizedSmallTalk.jinja",
    "PREV_LAST_REVIEW": "./prompts/PrevSessionReview.jinja",
    "DIALOGUE": "./prompts/Dialogue.jinja",
    "ROLEPLAYING": "./prompts/Roleplaying.jinja",
    "FREE_TALK": "./prompts/FreeTalk.jinja",
    "WRAP_UP": "./prompts/WrapUpClose.jinja",
}

reused_prompt = {
    "recastPrompt": """
    For each of the user's message, check if it's grammatically correct and natural. If not, naturally recast the user's message to provide an IMPLICIT corrective feedback. Do not directly correct the user's mistake. If appropriate, ask a simple and short follow-up question for each response.
    """
}
user_info = {
    "userName": "Chanhee",
    "userAge": 24,
    "userGender": "Female",
    "userNationality": "Korean",
    "userCompany": "StudyMax",
    "userPosition": "Prompt Engineer",
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
    "pastConversation": "The user just joined a start-up, StudyMax.",
    "todayExpression": "well known for",
}
