from functools import lru_cache
from uuid import UUID

from langchain_core.messages import AIMessage, HumanMessage, messages_from_dict
from sqlalchemy import select
from sqlalchemy.orm import Session

from agent.multi_agent import dispatch
# from agent.rag import RagService
from database.models import AgentChatMessage, ChatSession
from database.session import SessionLocal


def _normalize_session_id(session_id: str) -> str:
    return str(UUID(session_id))


def ensure_chat_session(session_id: str, user_id: int) -> str:
    sid = _normalize_session_id(session_id)
    with SessionLocal() as db:
        exists = db.scalar(select(ChatSession.id).where(ChatSession.id == sid))
        if exists is None:
            db.add(ChatSession(id=sid, user_id=user_id))
            db.commit()
    return sid


def chat_invoke(question: str, session_id: str, user_id: int) -> str:
    ensure_chat_session(session_id, user_id)
    return dispatch(question, session_id)


def serialize_chat_session(session: ChatSession) -> dict:
    return {
        "id": session.id,
        "user_id": session.user_id,
        "created_at": session.created_at.isoformat() if session.created_at else "",
        "updated_at": session.updated_at.isoformat() if session.updated_at else "",
    }


def _payload_to_chat_message(payload: dict) -> dict | None:
    for msg in messages_from_dict([payload]):
        if isinstance(msg, HumanMessage):
            content = msg.content
            if content:
                return {"role": "user", "content": str(content)}
        elif isinstance(msg, AIMessage):
            content = msg.content
            if isinstance(content, str) and content.strip():
                return {"role": "assistant", "content": content}
    return None


def _load_session_messages(db: Session, session_id: str) -> list[dict]:
    rows = db.scalars(
        select(AgentChatMessage)
        .where(AgentChatMessage.session_id == session_id)
        .order_by(AgentChatMessage.updated_at.desc())
    ).all()
    messages: list[dict] = []
    for row in rows:
        chat_message = _payload_to_chat_message(row.payload)
        if chat_message:
            messages.append(chat_message)
    return messages


def get_current_user_sessions(db: Session, user_id: int) -> list[ChatSession]:
    stmt = (
        select(ChatSession)
        .where(ChatSession.user_id == user_id)
        .order_by(ChatSession.updated_at.desc())
    )
    return db.scalars(stmt).all()


def get_chat_session_by_id(db: Session, session_id: str, user_id: int) -> ChatSession | None:
    sid = _normalize_session_id(session_id)
    stmt = select(ChatSession).where(ChatSession.id == sid, ChatSession.user_id == user_id)
    return db.scalar(stmt)


def get_chat_session_detail(db: Session, session_id: str, user_id: int) -> dict:
    session = get_chat_session_by_id(db, session_id, user_id)
    if session is None:
        raise ValueError("会话不存在")
    return {
        "session": serialize_chat_session(session),
        "messages": _load_session_messages(db, session.id),
    }
