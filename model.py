"""
+----------------------------------------------------------------------+
| Copyright (c) 2024 WeaversBrain. co. Ltd
+----------------------------------------------------------------------+
| 작업일 : 2024-05-23
| 파일설명 : 
+----------------------------------------------------------------------+
| 작업자 : 김용성, 박범열
+----------------------------------------------------------------------+
| 수정이력
|
+----------------------------------------------------------------------+ 
"""

from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ChatModel(BaseModel):
    chatId: int


class CreateChatModel(BaseModel):
    userId: int = 0
    userName: Optional[str] = None
    teacherName: Optional[str] = None
    teacherPersona: Optional[str] = None
    # messages: Optional[str] = None
    # chatTurn: int = 0
    # currentModule: int = 0


class ModuleModel(BaseModel):
    userId: int = 0
    chatId: int = 0
    module: Optional[str] = None
    userMessage: Optional[str] = None
