import os
from functools import lru_cache

from agent.rag import RagService


@lru_cache(maxsize=1)
def get_rag_service() -> RagService:
    return RagService()


def chat_invoke(question: str, session_id: str | None = None) -> str:
    # sid = session_id or os.getenv("DEFAULT_CHAT_SESSION_ID", "00000000-0000-0000-0000-000000000001")
    uuid_mock = "00000000-0000-0000-0000-000000000001"
    session_config = {"configurable": {"session_id": uuid_mock}}
    return get_rag_service().chain.invoke({"input": question}, session_config)
