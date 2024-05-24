from fastapi import FastAPI
from prompt_base import *
from app.utility import renderTemplate
import datetime

renderData = {}

######################################
#유저 정보 세팅
######################################
userInfo = {
    'userName': 'BeomYeol',
    'userAge': 24,
    'userGender': 'Female',
    'userNationality': 'Korean',
    'userCompany': 'StudyMax',
    'userPosition': 'Prompt Engineer',
}

######################################
#튜터 정보 세팅
######################################
tutorInfo = {
    'teacherPersona': 'You are an actual human English tutor, not an AI or GPT. Your name is Linda Bailey. Below is your personal information. Female, 34 years old, Caucasian, Blonde, Green eyes, approximately 5 feet 5 inches tall, living in Springfield, Illinois Undergraduate degree, majored in Communications, have a younger sister and a younger brother, have been tutoring ESL students fo 7 years, patient, nice, eager to teach, and eager to learn.',
    'teacherTimezone': 'America/Chicago'
}

######################################
#기타 필요 정보 세팅
######################################
otherInfo = {
    'currentTime':  'User Timezone: ' + str(datetime.datetime.now(kst)) + ' / Assistant Timezone: ' + str(datetime.datetime.now(cdt)),
    'currentLocation': 'User Location: South Korea',
    'pastConversation': 'The user just joined a start-up, StudyMax.',
    'todayExpression': 'well known for',
}

renderData.update(userInfo)
renderData.update(tutorInfo)
renderData.update(otherInfo)


######################################
#initial 모듈 랜더링
######################################
fakeModuleName = 'initial'
fakeRenderData = {
    'userName': 'BeomYeol',
    'teacherPersona': 'You are an actual human English tutor, not an AI or GPT. Your name is Linda Bailey. Below is your personal information. Female, 34 years old, Caucasian, Blonde, Green eyes, approximately 5 feet 5 inches tall, living in Springfield, Illinois Undergraduate degree, majored in Communications, have a younger sister and a younger brother, have been tutoring ESL students fo 7 years, patient, nice, eager to teach, and eager to learn.'
}

initialRendered = renderTemplate(fakeModuleName, fakeRenderData)


#히스토리 체크
#히스토리 내역

######################################
#모듈 랜더링
######################################
moduleName = 'smallTalk'
renderData = {}

if moduleName == 'smallTalk':
    renderData = {
        'currentTime': kst,

    }


print(initialRendered)


#llm 답변 리스턴스



