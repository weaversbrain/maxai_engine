from fastapi import APIRouter, Depends

router = APIRouter()

@router.post("/create")
def createChat():
    return {"chatId": 1}