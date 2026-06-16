import config  # noqa: F401 — 加载 server/.env

import os
import re

import streamlit as st

from auth import get_current_user, register

EMAIL_PATTERN = re.compile(r"^.+@.+\..+$")

st.set_page_config(page_title="注册", page_icon="📝", layout="centered")

if get_current_user():
    st.success(f"已登录：{get_current_user()['email']}")
    if st.button("进入智能客服", type="primary", use_container_width=True):
        st.switch_page("app.py")
    st.stop()

st.title("📝 注册")
st.caption("注册后请登录，再使用 Agent 智能对话")

with st.form("register_form"):
    email = st.text_input("邮箱", placeholder="name@example.com")
    password = st.text_input("密码", type="password", placeholder="6-8 位")
    submitted = st.form_submit_button("注册", type="primary", use_container_width=True)

if submitted:
    if not EMAIL_PATTERN.match(email.strip()):
        st.error("请输入有效的邮箱地址")
    elif len(password) < 6:
        st.error("密码长度至少 6 位")
    else:
        with st.spinner("注册中..."):
            try:
                register(email.strip(), password)
                st.success("注册成功，请登录")
                st.switch_page("pages/login.py")
            except RuntimeError as exc:
                st.error(str(exc))

st.divider()
st.page_link("pages/login.py", label="已有账号？前往登录", icon="🔐")

grpc_target = f"{os.environ.get('GRPC_HOST', '127.0.0.1')}:{os.environ.get('GRPC_PORT', '50051')}"
st.caption(f"gRPC 服务地址：{grpc_target}")
