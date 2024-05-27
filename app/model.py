from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ChatModel(BaseModel):
    chatId: int

class createChatModel(BaseModel):
    userId: int
    userName: Optional[str] = None
    teacherName: Optional[str] = None
    teacherPersona: Optional[str] = None