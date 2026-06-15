import config  # noqa: F401 — 加载 server/.env

import os

import streamlit as st

from rag_service import ask

st.set_page_config(
    page_title="文档中心智能客服",
    page_icon="💬",
    layout="centered",
)

st.title("💬 文档中心智能客服")
st.caption("基于知识库的智能问答，请先在后管系统中上传并向量化文档")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if message["role"] == "assistant" and message.get("sources"):
            with st.expander("参考来源"):
                for src in message["sources"]:
                    st.markdown(f"**[{src['index']}] 来源 {src['source']}**")
                    st.text(src["content"][:300] + ("..." if len(src["content"]) > 300 else ""))

if prompt := st.chat_input("请输入您的问题..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("思考中..."):
            try:
                result = ask(prompt)
                st.markdown(result["answer"])
                if result["sources"]:
                    with st.expander("参考来源"):
                        for src in result["sources"]:
                            st.markdown(f"**[{src['index']}] 来源 {src['source']}**")
                            st.text(
                                src["content"][:300]
                                + ("..." if len(src["content"]) > 300 else "")
                            )
                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": result["answer"],
                        "sources": result["sources"],
                    }
                )
            except Exception as e:
                error_msg = f"抱歉，服务暂时不可用：{e}"
                st.error(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg})

with st.sidebar:
    st.header("使用说明")
    st.markdown(
        """
        1. 在**后管系统**上传文档
        2. 对文档执行**向量化**操作
        3. 回到此处提问，客服将基于知识库回答
        """
    )
    st.page_link("pages/register.py", label="客户注册", icon="📝")
    if st.session_state.get("registered_client"):
        st.info(f"当前客户：{st.session_state.registered_client['email']}")
    if st.button("清空对话"):
        st.session_state.messages = []
        st.rerun()

    if not os.environ.get("DASHSCOPE_API_KEY"):
        st.warning("未检测到 DASHSCOPE_API_KEY，请检查 server/.env 配置")
