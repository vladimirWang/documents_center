from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database.session import get_db
from agent.rag import RagService
from module_chat.chat_service import chat_invoke
from module_chat.chat_vo import ChatRequest
from common.resp import BaseResp

chat_router = APIRouter(
    prefix="/chat",
    tags=["聊天"],
)

@chat_router.post("/")
def chat(request: ChatRequest, db: Session = Depends(get_db)):
    result = chat_invoke(request.question, request.session_id)
    j = request.model_dump()
    
    print("request: ", j)
    return BaseResp.success(result)