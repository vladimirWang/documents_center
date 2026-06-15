import config  # noqa: F401 — 加载 server/.env

import streamlit as st

from chat_ui import render_chat_page

st.set_page_config(
    page_title="新对话",
    page_icon="➕",
    layout="centered",
)

render_chat_page()
