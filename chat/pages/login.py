import config  # noqa: F401 — 加载 server/.env

import re

import streamlit as st

from auth import get_current_user, login

EMAIL_PATTERN = re.compile(r"^.+@.+\..+$")

st.set_page_config(page_title="登录", page_icon="🔐", layout="centered")

if get_current_user():
    st.success(f"已登录：{get_current_user()['email']}")
    if st.button("进入智能客服", type="primary", use_container_width=True):
        st.switch_page("app.py")
    st.stop()

st.title("🔐 登录")
st.caption("登录后可使用 Agent 智能对话")

with st.form("login_form"):
    email = st.text_input("邮箱", placeholder="name@example.com")
    password = st.text_input("密码", type="password")
    submitted = st.form_submit_button("登录", type="primary", use_container_width=True)

if submitted:
    if not EMAIL_PATTERN.match(email.strip()):
        st.error("请输入有效的邮箱地址")
    elif not password:
        st.error("请输入密码")
    else:
        with st.spinner("登录中..."):
            try:
                user = login(email.strip(), password)
                st.success(f"欢迎，{user['username'] or user['email']}")
                st.switch_page("app.py")
            except RuntimeError as exc:
                st.error(str(exc))

st.divider()
st.page_link("pages/register.py", label="没有账号？立即注册", icon="📝")
