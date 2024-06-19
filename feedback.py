"""
+----------------------------------------------------------------------+
| Copyright (c) 2024 WeaversBrain. co. Ltd
+----------------------------------------------------------------------+
| 작업일 : 2024-05-23
| 파일설명 : 피드백
+----------------------------------------------------------------------+
| 작업자 : 박범열
+----------------------------------------------------------------------+
| 수정이력
|
+----------------------------------------------------------------------+ 
"""

from openai import OpenAI
from dotenv import load_dotenv
from model import CreateFeedbackModel
from crud import *
from utility import *
from dotenv import dotenv_values
import os


def createFeedback(createFeedbackModel):
    print(1)
