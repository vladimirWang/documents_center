from fastapi import APIRouter, Depends, HTTPException
from deps.verify_token import verify_token
from sqlalchemy.orm import Session
from database.session import get_db
from agent.rag import RagService
from module_chat.chat_service import chat_invoke
from module_chat.chat_vo import ChatRequest
from common.resp import BaseResp
from database.models import ChatSession
from sqlalchemy import select
from module_chat.chat_service import (
    get_chat_session_detail,
    get_current_user_sessions,
    serialize_chat_session,
)

chat_router = APIRouter(
    prefix="/chat",
    tags=["聊天"],
)

@chat_router.post("/")
def chat(request: ChatRequest, db: Session = Depends(get_db), user_info: dict = Depends(verify_token),):
    result = chat_invoke(request.question, request.session_id, user_info["user_id"])
    return BaseResp.success(result)

@chat_router.get("/sessions")
def get_sessions(db: Session = Depends(get_db), user_info: dict = Depends(verify_token)):
    db_sessions = get_current_user_sessions(db, user_info["user_id"])
    return BaseResp.success(
        {"sessions": [serialize_chat_session(session) for session in db_sessions]}
    )


@chat_router.get("/sessions/{session_id}")
def get_session(session_id: str, db: Session = Depends(get_db), user_info: dict = Depends(verify_token)):
    try:
        detail = get_chat_session_detail(db, session_id, user_info["user_id"])
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return BaseResp.success(detail)