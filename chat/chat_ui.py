import config  # noqa: F401 — 加载 server/.env

import os
import uuid

import streamlit as st

from auth import logout, require_login
from grpc_client import get_chat_session_by_id, list_user_sessions
from rag_service import ask

SESSION_KEY = "session_id"
MESSAGES_KEY = "messages"
USAGE_HELP = (
    "1. 在「后管系统」上传文档\n"
    "2. 对文档执行「向量化」操作\n"
    "3. 回到此处提问，客服将基于知识库回答"
)


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


def _format_session_time(value: str) -> str:
    if not value:
        return "-"
    return value.replace("T", " ")[:19]


def _switch_session(session_id: str, user_id: int) -> None:
    detail = get_chat_session_by_id(session_id, user_id)
    st.session_state[SESSION_KEY] = session_id
    if MESSAGES_KEY not in st.session_state:
        st.session_state[MESSAGES_KEY] = {}
    st.session_state[MESSAGES_KEY][session_id] = detail["messages"]
    st.rerun()


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

    title_col, help_col, action_col = st.columns([7.2, 0.5, 1], vertical_alignment="center")
    with title_col:
        st.title("💬 智能助手")
        st.caption("基于知识库的智能问答，请先在后管系统中上传并向量化文档")
    with help_col:
        st.button("ℹ️", help=USAGE_HELP, key="usage_help", type="tertiary")
    with action_col:
        if st.button("➕", help="新对话", use_container_width=True):
            _start_new_conversation()

    # st.caption(f"当前用户：{user['email']} · 会话：{session_id[:8]}…")

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
        st.header("历史会话")
        try:
            sessions = list_user_sessions(user["user_id"])
            if not sessions:
                st.caption("暂无历史会话")
            for item in sessions:
                sid = item["id"]
                label = f"{sid[:8]}… · {_format_session_time(item['updated_at'])}"
                button_type = "primary" if sid == session_id else "secondary"
                if st.button(label, key=f"session_{sid}", use_container_width=True, type=button_type):
                    if sid != session_id:
                        _switch_session(sid, user["user_id"])
        except Exception as e:
            st.error(f"加载会话失败：{e}")

        st.divider()
        # st.info(f"当前用户：{user['email']}（ID: {user['user_id']}）")
        if st.button("退出登录"):
            logout()
            st.switch_page("pages/login.py")
        if st.button("清空当前对话"):
            messages.clear()
            st.rerun()

        if not os.environ.get("DASHSCOPE_API_KEY"):
            st.warning("未检测到 DASHSCOPE_API_KEY，请检查 server/.env 配置")
