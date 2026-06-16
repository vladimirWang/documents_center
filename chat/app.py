import config  # noqa: F401 — 加载 server/.env

import streamlit as st

from auth import get_current_user
from chat_ui import render_chat_page

st.set_page_config(
    page_title="文档中心智能客服",
    page_icon="💬",
    layout="centered",
)

if not get_current_user():
    st.switch_page("pages/login.py")

render_chat_page()
