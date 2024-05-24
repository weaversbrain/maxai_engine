import pytz

templateList = {
    'initial': './prompts/InitialSystemPrompt.jinja',
    'smallTalk': './prompts/PersonalizedSmallTalk.jinja',
    'reviewLastClass': './prompts/PrevSessionReview.jinja',
    'dialogue': './prompts/Dialogue.jinja',
    'roleplaying': './prompts/Roleplaying.jinja',
    'freeTalk': './prompts/FreeTalk.jinja',
    'wrapup': './prompts/WrapUpClose.jinja'
}
reused_prompt = {
    'recastPrompt':
    '''
    For each of the user's message, check if it's grammatically correct and natural. If not, naturally recast the user's message to provide an IMPLICIT corrective feedback. Do not directly correct the user's mistake. If appropriate, ask a simple and short follow-up question for each response.
    '''
}

kst = pytz.timezone('Asia/Seoul')
cdt = pytz.timezone('America/Chicago')