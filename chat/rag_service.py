import config  # noqa: F401 — 初始化环境变量与 server 模块路径

from grpc_client import ask_chat


def ask(question: str, session_id: str, user_id: int) -> dict:
    answer = ask_chat(question, session_id, user_id)
    return {"answer": answer, "sources": []}
