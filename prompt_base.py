import datetime
import pytz

templates = {
    "INITIAL": "./prompts/InitialSystemPrompt.jinja",
    "E6_SMALL_TALK": "./prompts/PersonalizedSmallTalk.jinja",
    "E6_REVIEW_LAST_CLASS": "./prompts/PrevSessionReview.jinja",
    "E6_DIALOGUE": "./prompts/Dialogue.jinja",
    "E6_ROLEPLAYING": "./prompts/Roleplaying.jinja",
    "E6_TALK_MORE": "./prompts/FreeTalk.jinja",
    "E6_WRAP_UP": "./prompts/WrapUpClose.jinja",
}

reused_prompt = {
    "recastPrompt": """
    For each of the user's message, check if it's grammatically correct and natural. If not, naturally recast the user's message to provide an IMPLICIT corrective feedback. Do not directly correct the user's mistake. If appropriate, ask a simple and short follow-up question for each response.
    """
}

kst = pytz.timezone("Asia/Seoul")
cdt = pytz.timezone("America/Chicago")

other_data = {
    "currentTime": "User Timezone: "
    + str(datetime.datetime.now(kst))
    + " / Assistant Timezone: "
    + str(datetime.datetime.now(cdt)),
    "currentLocation": "User Location: South Korea",
    "pastConversation": "The user just joined a start-up, StudyMax.",
}
