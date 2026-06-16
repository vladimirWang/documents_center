import config  # noqa: F401 — 加载 server/.env

import os
import uuid

import streamlit as st

from auth import logout, require_login
from rag_service import ask

SESSION_KEY = "session_id"
MESSAGES_KEY = "messages"


def _current_session_id() -> str:
    if SESSION_KEY not in st.session_state:
        st.session_state[SESSION_KEY] = str(uuid.uuid4())
    return st.session_state[SESSION_KEY]


def _current_messages() -> list:
    sid = _current_session_id()
    if MESSAGES_KEY not in st.session_state:
        st.session_state[MESSAGES_KEY] = {}
    if sid not in st.session_state[MESSAGES_KEY]:
        st.session_state[MESSAGES_KEY][sid] = []
    return st.session_state[MESSAGES_KEY][sid]


def _start_new_conversation() -> None:
    new_session_id = str(uuid.uuid4())
    st.session_state[SESSION_KEY] = new_session_id
    if MESSAGES_KEY not in st.session_state:
        st.session_state[MESSAGES_KEY] = {}
    st.session_state[MESSAGES_KEY][new_session_id] = []
    st.switch_page("pages/conversation.py")


def render_chat_page() -> None:
    user = require_login()
    session_id = _current_session_id()
    messages = _current_messages()

    title_col, action_col = st.columns([8, 1])
    with title_col:
        st.title("💬 文档中心智能客服")
        st.caption("基于知识库的智能问答，请先在后管系统中上传并向量化文档")
    with action_col:
        st.write("")
        if st.button("➕", help="新对话", use_container_width=True):
            _start_new_conversation()

    st.caption(f"当前用户：{user['email']} · 会话：{session_id[:8]}…")

    for message in messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            if message["role"] == "assistant" and message.get("sources"):
                with st.expander("参考来源"):
                    for src in message["sources"]:
                        st.markdown(f"**[{src['index']}] 来源 {src['source']}**")
                        st.text(src["content"][:300] + ("..." if len(src["content"]) > 300 else ""))

    if prompt := st.chat_input("请输入您的问题..."):
        messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("思考中..."):
                try:
                    print("----user_id----: ", user["user_id"])
                    result = ask(prompt, session_id, user["user_id"])
                    st.markdown(result["answer"])
                    if result["sources"]:
                        with st.expander("参考来源"):
                            for src in result["sources"]:
                                st.markdown(f"**[{src['index']}] 来源 {src['source']}**")
                                st.text(
                                    src["content"][:300]
                                    + ("..." if len(src["content"]) > 300 else "")
                                )
                    messages.append(
                        {
                            "role": "assistant",
                            "content": result["answer"],
                            "sources": result["sources"],
                        }
                    )
                except Exception as e:
                    error_msg = f"抱歉，服务暂时不可用：{e}"
                    st.error(error_msg)
                    messages.append({"role": "assistant", "content": error_msg})

    with st.sidebar:
        st.header("使用说明")
        st.markdown(
            """
            1. 在**后管系统**上传文档
            2. 对文档执行**向量化**操作
            3. 回到此处提问，客服将基于知识库回答
            """
        )
        st.page_link("pages/login.py", label="登录", icon="🔐")
        st.page_link("pages/register.py", label="注册", icon="📝")
        st.info(f"当前用户：{user['email']}（ID: {user['user_id']}）")
        if st.button("退出登录"):
            logout()
            st.switch_page("pages/login.py")
        if st.button("清空当前对话"):
            messages.clear()
            st.rerun()

        if not os.environ.get("DASHSCOPE_API_KEY"):
            st.warning("未检测到 DASHSCOPE_API_KEY，请检查 server/.env 配置")
