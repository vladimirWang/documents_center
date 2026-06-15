import config  # noqa: F401 — 初始化环境变量与 server 模块路径

import os

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

import agent.config_data as agent_config
from agent.pgvector_store import get_pgvector_store

SYSTEM_PROMPT = """你是文档中心的智能客服助手，请根据提供的知识库内容回答用户问题。

要求：
1. 优先使用知识库中的信息作答，回答要准确、简洁、友好。
2. 如果知识库中没有相关信息，请诚实告知用户，并给出通用建议。
3. 使用中文回答。"""

PROMPT = ChatPromptTemplate.from_messages(
    [
        ("system", SYSTEM_PROMPT),
        (
            "human",
            "知识库参考内容：\n{context}\n\n用户问题：{question}",
        ),
    ]
)


def _get_llm() -> ChatOpenAI:
    api_key = os.environ.get("DASHSCOPE_API_KEY")
    if not api_key:
        raise RuntimeError("未配置 DASHSCOPE_API_KEY，请在 server/.env 中设置")
    return ChatOpenAI(
        model=agent_config.chat_model_name,
        api_key=api_key,
        base_url=os.environ.get(
            "DASHSCOPE_BASE_URL",
            "https://dashscope.aliyuncs.com/compatible-mode/v1",
        ),
        temperature=0.3,
    )


def _retrieve_context(question: str) -> tuple[str, list[dict]]:
    store = get_pgvector_store()
    retriever = store.as_retriever(search_kwargs={"k": agent_config.search_kwargs})
    docs = retriever.invoke(question)

    if not docs:
        return "（暂无相关知识库内容）", []

    context_parts = []
    sources = []
    for i, doc in enumerate(docs, start=1):
        source = (doc.metadata or {}).get("source", "未知")
        context_parts.append(f"[{i}] {doc.page_content}")
        sources.append({"index": i, "source": source, "content": doc.page_content})

    return "\n\n".join(context_parts), sources


def ask(question: str) -> dict:
    context, sources = _retrieve_context(question)
    chain = PROMPT | _get_llm() | StrOutputParser()
    answer = chain.invoke({"context": context, "question": question})
    return {"answer": answer, "sources": sources}
