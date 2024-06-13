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


class CreateChatModel(BaseModel):
    userId: int = 0
    lessonId: int = 0
    userName: Optional[str] = None
    teacherName: Optional[str] = None
    teacherPersona: Optional[str] = None


class CreateHistoryModel(BaseModel):
    chatId: int = 0
    userId: int = 0
    speaker: Optional[str] = None
    message: Optional[str] = None
    module: Optional[str] = None
    chatTurn: int = 0


class ModuleModel(BaseModel):
    chatId: int = 0
    moduleId: int = 0
    userAnswer: Optional[str] = None


class HistoryModel(BaseModel):
    type: Optional[str] = None
    whereData: Optional[dict] = None


class ModuleListData(BaseModel):
    lessonId: int = 0
