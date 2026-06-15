import config  # noqa: F401 — 初始化环境变量与 server 模块路径

from grpc_client import ask_chat


def ask(question: str) -> dict:
    answer = ask_chat(question)
    return {"answer": answer, "sources": []}
