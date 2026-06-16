import os
from functools import lru_cache
from uuid import UUID

from sqlalchemy import select

from agent.multi_agent import dispatch
from agent.rag import RagService
from database.models import ChatSession
from database.session import SessionLocal


@lru_cache(maxsize=1)
def get_rag_service() -> RagService:
    return RagService()


def _normalize_session_id(session_id: str) -> str:
    return str(UUID(session_id))


def ensure_chat_session(session_id: str, user_id: int | None = None) -> str:
    sid = _normalize_session_id(session_id)
    uid = user_id or int(os.getenv("DEFAULT_CHAT_USER_ID", "1"))
    with SessionLocal() as db:
        exists = db.scalar(select(ChatSession.id).where(ChatSession.id == sid))
        if exists is None:
            db.add(ChatSession(id=sid, user_id=uid))
            db.commit()
    return sid


def chat_invoke(question: str, session_id: str) -> str:
    return dispatch(question, session_id, get_rag_service())
